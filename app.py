from flask import Flask, redirect, render_template, request, url_for, session, jsonify, send_file, flash
from werkzeug.utils import secure_filename
import mysql.connector
import time
import os
from datetime import datetime, timedelta
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import bcrypt
from ollama import chat, embed
import json
import math
import uuid
import threading
import re
import base64
from otp import send_otp_sms
from profanity import check_profanity

app = Flask(__name__)
app.secret_key = 'actbayan_secret_key_2026'


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="actbayan"
    )


def hash_password_bcrypt(password: str) -> str:
    if password is None:
        password = ""
    pw_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password_bcrypt(stored_hash, password: str) -> bool:
    if stored_hash is None or password is None:
        return False

    if isinstance(stored_hash, (bytes, bytearray)):
        hash_bytes = bytes(stored_hash)
    else:
        hash_bytes = str(stored_hash).encode('utf-8')

    return bcrypt.checkpw(password.encode('utf-8'), hash_bytes)


# ===== OLLAMA DUPLICATE DETECTION HELPERS =====
def get_embedding(text):
    """Generate embedding vector for text using Ollama nomic-embed-text"""
    try:
        response = embed(
            model='nomic-embed-text',
            input=text
        )
        if response and 'embeddings' in response:
            return response['embeddings'][0]
        return None
    except Exception as e:
        print(f"[Ollama] Embedding error: {e}")
        return None


def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two vectors"""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def haversine_distance(lat1, lng1, lat2, lng2):
    """Compute distance in meters between two GPS coordinates"""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    delta_phi = math.radians(float(lat2) - float(lat1))
    delta_lambda = math.radians(float(lng2) - float(lng1))
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def text_similarity(text1, text2):
    """Compare two texts using Ollama embeddings and cosine similarity"""
    if not text1 or not text2:
        return 0.0
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    if not emb1 or not emb2:
        return 0.0
    return cosine_similarity(emb1, emb2)


def coordinate_proximity(lat1, lng1, lat2, lng2, threshold_meters=100):
    """Check if two coordinates are within threshold meters of each other"""
    try:
        lat1_f = float(lat1)
        lng1_f = float(lng1)
        lat2_f = float(lat2)
        lng2_f = float(lng2)
        if lat1_f == 0 and lng1_f == 0:
            return False, float('inf')
        if lat2_f == 0 and lng2_f == 0:
            return False, float('inf')
        distance = haversine_distance(lat1_f, lng1_f, lat2_f, lng2_f)
        return distance <= threshold_meters, distance
    except (ValueError, TypeError):
        return False, float('inf')


# ===== OLLAMA ANALYTICS SUMMARIZATION HELPER (CACHED & NON-BLOCKING) =====
_ANALYTICS_CACHE_V2 = {
    'time': 0,
    'monthly_summary': None,
    'sample_summary': None,
    'status_summary': None,
    'location_summary': None,
    'category_summary': None,
    'executive_summary': None,
    'is_generating': False
}


def _run_ollama_in_background(monthly_labels, monthly_counts, monthly_resolved, sample_report, fallback_summary, fallback_sample_summary, fallback_status_summary, status_counts, top_locations, fallback_location_summary, category_data, fallback_category_summary, fallback_executive_summary=''):
    global _ANALYTICS_CACHE_V2
    executive_part = fallback_executive_summary
    try:
        sample_info = ""
        if sample_report:
            sample_info = (
                f"\nSample Citizen Report (From Past Week / Community):\n"
                f"- Title: {sample_report.get('title')}\n"
                f"- Category: {sample_report.get('category')}\n"
                f"- Location: {sample_report.get('locname') or 'Barangay Picaleon'}\n"
                f"- Status: {sample_report.get('status')}\n"
                f"- Description: {sample_report.get('description')}\n"
            )

        total_volume = sum(monthly_counts) if monthly_counts else 0
        total_resolved = sum(monthly_resolved) if monthly_resolved else 0
        resolution_pct = round((total_resolved / total_volume) * 100) if total_volume > 0 else 0
        peak_count = max(monthly_counts) if monthly_counts else 0
        peak_month = monthly_labels[monthly_counts.index(peak_count)] if peak_count > 0 and monthly_counts else 'N/A'

        status_info = (
            f"\nCurrent Status Breakdown:\n"
            f"- Total: {status_counts.get('total', 0)}\n"
            f"- Pending: {status_counts.get('pending', 0)}\n"
            f"- In Progress: {status_counts.get('in_progress', 0)}\n"
            f"- Resolved: {status_counts.get('resolved', 0)}\n"
            f"- Denied: {status_counts.get('denied', 0)}\n"
        )

        loc_info = ""
        if top_locations:
            loc_list = ", ".join([f"{loc.get('locname', 'Unknown')} ({loc.get('count', 0)})" for loc in top_locations[:5]])
            loc_info = f"\nTop Locations:\n- {loc_list}\n"

        cat_info = ""
        if category_data:
            cat_list = ", ".join([f"{c['name']} ({c['count']})" for c in category_data[:5]])
            cat_info = f"\nTop Categories:\n- {cat_list}\n"

        prompt = (
            f"You are a local government analytics assistant for Barangay Picaleon (ActBayan system).\n"
            f"Analyze this 6-month report volume data:\n"
            f"- Months: {', '.join(monthly_labels)}\n"
            f"- Submissions: {monthly_counts}\n"
            f"- Resolved: {monthly_resolved}\n"
            f"- Total: {total_volume}, Peak: {peak_month} ({peak_count} reports)\n"
            f"- Resolution rate: {resolution_pct}%\n"
            f"{status_info}"
            f"{sample_info}\n"
            f"{loc_info}"
            f"{cat_info}"
            f"Instructions:\n"
            f"1. Write a concise 1-2 sentence analytical summary of the monthly volume trend, including peak periods, trajectory, and resolution performance.\n"
            f"2. Write a concise 1-2 sentence analytical summary of the current status breakdown (Pending, In Progress, Resolved).\n"
            f"3. If a sample report is provided, write 1 sentence summarizing what that sample concern illustrates.\n"
            f"4. If location data is provided, write a detailed 3-4 sentence analytical summary of the top reported locations.\n"
            f"5. If category data is provided, write a concise 1-2 sentence analytical summary of the top reported concern categories.\n"
            f"6. Write a comprehensive 3-5 sentence EXECUTIVE SUMMARY that synthesizes all the data above.\n"
            f"CRITICAL: DO NOT use markdown formatting like **bolding** or bullet points in the output keys.\n"
            f"Output format:\n"
            f"TREND_SUMMARY: <1-2 sentence summary>\n"
            f"STATUS_SUMMARY: <1-2 sentence summary>\n"
            f"SAMPLE_SUMMARY: <1-sentence summary>\n"
            f"LOCATION_SUMMARY: <1-2 sentence summary>\n"
            f"CATEGORY_SUMMARY: <1-2 sentence summary>\n"
            f"EXECUTIVE_SUMMARY: <3-5 sentence executive overview>"
        )

        response = chat(
            model='llama3.2:3b',
            messages=[
                {'role': 'system', 'content': 'You are a detailed and analytical municipal data expert for Barangay Picaleon. Provide elaborate insights based on the data. Output only the requested summaries without conversational filler.'},
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': 0.4, 'num_predict': 500}
        )

        content = response.get('message', {}).get('content', '').strip()
        if content:
            content = content.replace('**', '')
            trend_part = fallback_summary
            status_part = fallback_status_summary
            sample_part = fallback_sample_summary
            location_part = fallback_location_summary
            category_part = fallback_category_summary

            if 'TREND_SUMMARY:' in content:
                parts = content.split('STATUS_SUMMARY:')
                trend_part = parts[0].replace('TREND_SUMMARY:', '').strip()
                if len(parts) > 1:
                    sub_parts = parts[1].split('SAMPLE_SUMMARY:')
                    status_part = sub_parts[0].strip()
                    if len(sub_parts) > 1:
                        loc_parts = sub_parts[1].split('LOCATION_SUMMARY:')
                        sample_part = loc_parts[0].strip()
                        if len(loc_parts) > 1:
                            cat_parts = loc_parts[1].split('CATEGORY_SUMMARY:')
                            location_part = cat_parts[0].strip()
                            if len(cat_parts) > 1:
                                exec_parts = cat_parts[1].split('EXECUTIVE_SUMMARY:')
                                category_part = exec_parts[0].strip()
                                if len(exec_parts) > 1:
                                    executive_part = exec_parts[1].strip()
            else:
                trend_part = content

            _ANALYTICS_CACHE_V2['monthly_summary'] = trend_part or fallback_summary
            _ANALYTICS_CACHE_V2['status_summary'] = status_part or fallback_status_summary
            _ANALYTICS_CACHE_V2['sample_summary'] = sample_part or fallback_sample_summary
            _ANALYTICS_CACHE_V2['location_summary'] = location_part or fallback_location_summary
            _ANALYTICS_CACHE_V2['category_summary'] = category_part or fallback_category_summary
            _ANALYTICS_CACHE_V2['executive_summary'] = executive_part or fallback_executive_summary
            _ANALYTICS_CACHE_V2['time'] = time.time()
            print("[Ollama Analytics] Successfully generated and cached AI summary.")
    except Exception as e:
        print(f"[Ollama Analytics] Background generation error: {e}")
    finally:
        _ANALYTICS_CACHE_V2['is_generating'] = False


def generate_monthly_analytics_summary(monthly_labels, monthly_counts, monthly_resolved, sample_report=None, status_counts=None, top_locations=None, category_data=None):
    global _ANALYTICS_CACHE_V2
    now = time.time()

    if _ANALYTICS_CACHE_V2.get('monthly_summary') and (now - _ANALYTICS_CACHE_V2.get('time', 0) < 900):
        return (
            _ANALYTICS_CACHE_V2['monthly_summary'],
            _ANALYTICS_CACHE_V2.get('sample_summary', ''),
            _ANALYTICS_CACHE_V2.get('status_summary', ''),
            _ANALYTICS_CACHE_V2.get('location_summary', ''),
            _ANALYTICS_CACHE_V2.get('category_summary', '')
        )

    total_volume = sum(monthly_counts) if monthly_counts else 0
    total_resolved = sum(monthly_resolved) if monthly_resolved else 0
    resolution_pct = round((total_resolved / total_volume) * 100) if total_volume > 0 else 0

    peak_count = max(monthly_counts) if monthly_counts else 0
    peak_month = monthly_labels[monthly_counts.index(peak_count)] if peak_count > 0 and monthly_counts else 'N/A'

    trend_direction = "stable"
    if len(monthly_counts) >= 2:
        last_m = monthly_counts[-1]
        prev_m = monthly_counts[-2]
        if last_m > prev_m:
            diff = last_m - prev_m
            pct_change = round((diff / prev_m * 100)) if prev_m > 0 else 100
            trend_direction = f"upward (+{pct_change}% vs previous month)"
        elif last_m < prev_m:
            diff = prev_m - last_m
            pct_change = round((diff / prev_m * 100)) if prev_m > 0 else 0
            trend_direction = f"downward (-{pct_change}% vs previous month)"

    fallback_summary = (
        f"Over the past 6 months, Barangay Picaleon received {total_volume} total citizen concerns, "
        f"peaking in {peak_month} with {peak_count} reports. The overall resolution rate stands at {resolution_pct}% "
        f"with a {trend_direction} reporting trajectory."
    )
    fallback_sample_summary = ""
    if sample_report:
        fallback_sample_summary = (
            f"A representative concern '{sample_report.get('title')}' in {sample_report.get('locname') or 'Barangay Picaleon'} "
            f"({sample_report.get('category')}) is currently {sample_report.get('status')}, "
            f"illustrating priority citizen feedback."
        )

    status_counts = status_counts or {}
    fallback_status_summary = (
        f"Out of {status_counts.get('total', 0)} total reports, {status_counts.get('resolved', 0)} have been fully resolved by the LGU team. "
        f"Currently, {status_counts.get('in_progress', 0)} reports are in progress and {status_counts.get('pending', 0)} reports are pending review."
    )

    fallback_location_summary = ""
    if top_locations:
        top_loc = top_locations[0]
        fallback_location_summary = f"The area with the highest volume of concerns is {top_loc.get('locname')} with {top_loc.get('count')} reports."

    fallback_category_summary = ""
    if category_data:
        top_cat = category_data[0]
        fallback_category_summary = f"The most reported concern category is {top_cat['name']} with {top_cat['count']} reports."

    s = status_counts or {}
    res_pct = round((s.get('resolved', 0) / s.get('total', 1)) * 100) if s.get('total', 0) > 0 else 0
    top_loc_name = top_locations[0].get('locname', 'N/A') if top_locations else 'N/A'
    top_cat_name = category_data[0]['name'] if category_data else 'N/A'
    fallback_executive_summary = (
        f"Barangay Picaleon's ActBayan system currently manages {s.get('total', 0)} total citizen concerns "
        f"with a {res_pct}% overall resolution rate. "
        f"The {top_cat_name} category leads in volume, and {top_loc_name} is the most active reporting area. "
        f"There are currently {s.get('pending', 0)} pending reports requiring immediate LGU attention, "
        f"while {s.get('in_progress', 0)} are actively being handled. "
        f"The LGU team is encouraged to prioritize the backlog to improve community satisfaction."
    )

    if not _ANALYTICS_CACHE_V2.get('is_generating', False):
        _ANALYTICS_CACHE_V2['is_generating'] = True
        t = threading.Thread(
            target=_run_ollama_in_background,
            args=(monthly_labels, monthly_counts, monthly_resolved, sample_report, fallback_summary, fallback_sample_summary, fallback_status_summary, status_counts, top_locations, fallback_location_summary, category_data, fallback_category_summary, fallback_executive_summary),
            daemon=True
        )
        t.start()

    if not _ANALYTICS_CACHE_V2.get('monthly_summary'):
        _ANALYTICS_CACHE_V2['monthly_summary'] = fallback_summary
        _ANALYTICS_CACHE_V2['sample_summary'] = fallback_sample_summary
        _ANALYTICS_CACHE_V2['status_summary'] = fallback_status_summary
        _ANALYTICS_CACHE_V2['location_summary'] = fallback_location_summary
        _ANALYTICS_CACHE_V2['category_summary'] = fallback_category_summary
        _ANALYTICS_CACHE_V2['executive_summary'] = fallback_executive_summary
        _ANALYTICS_CACHE_V2['time'] = now

    return (
        _ANALYTICS_CACHE_V2['monthly_summary'],
        _ANALYTICS_CACHE_V2.get('sample_summary', ''),
        _ANALYTICS_CACHE_V2.get('status_summary', ''),
        _ANALYTICS_CACHE_V2.get('location_summary', ''),
        _ANALYTICS_CACHE_V2.get('category_summary', '')
    )


# ===== API: Get Analytics Summary =====
@app.route('/api/analytics_summary')
def api_analytics_summary():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return {'success': False, 'message': 'Unauthorized'}, 401
    return {
        'success': True,
        'monthly_summary': _ANALYTICS_CACHE_V2.get('monthly_summary', ''),
        'sample_summary': _ANALYTICS_CACHE_V2.get('sample_summary', ''),
        'status_summary': _ANALYTICS_CACHE_V2.get('status_summary', ''),
        'location_summary': _ANALYTICS_CACHE_V2.get('location_summary', ''),
        'category_summary': _ANALYTICS_CACHE_V2.get('category_summary', ''),
        'executive_summary': _ANALYTICS_CACHE_V2.get('executive_summary', ''),
        'is_generating': _ANALYTICS_CACHE_V2.get('is_generating', False)
    }


# ===== API: Force Regenerate Analytics Summary =====
@app.route('/api/analytics_summary/regenerate', methods=['POST'])
def api_analytics_summary_regenerate():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return {'success': False, 'message': 'Unauthorized'}, 401
    global _ANALYTICS_CACHE_V2
    _ANALYTICS_CACHE_V2 = {
        'time': 0,
        'monthly_summary': None,
        'sample_summary': None,
        'status_summary': None,
        'location_summary': None,
        'category_summary': None,
        'executive_summary': None,
        'is_generating': False
    }
    return {'success': True, 'message': 'Cache cleared. Refresh the analytics page to regenerate.'}


# ===== API: Get Reports by Category =====
@app.route('/api/reports')
def api_reports():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return {'success': False, 'message': 'Unauthorized'}, 401

    category = request.args.get('category')
    if not category:
        return {'success': False, 'message': 'Category required'}, 400

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    query = """
        SELECT r.report_id, r.title, 'General' AS category, r.status, r.created_at,
               a.first_name, a.last_name, '' AS profile_photo,
               CONCAT(l.x, ', ', l.y) AS locname
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        LEFT JOIN location l ON r.location_id = l.location_id
        ORDER BY r.created_at DESC
        LIMIT 50
    """
    cursor.execute(query)
    reports = cursor.fetchall()
    con.close()

    for r in reports:
        if r.get('created_at'):
            r['created_at_str'] = r['created_at'].strftime('%b %d')
        else:
            r['created_at_str'] = '�?"'

        r['first_name'] = r.get('first_name') or 'Resident'
        r['last_name'] = r.get('last_name') or ''
        r['locname'] = r.get('locname') or '�?"'
        r['status'] = r.get('status') or 'Pending'

    return {'success': True, 'reports': reports}


# ===== API: Check for duplicate concerns =====
@app.route('/api/check_duplicate', methods=['POST'])
def api_check_duplicate():
    if 'user_id' not in session:
        return {'success': False, 'message': 'Not logged in'}, 401

    data = request.get_json()
    if not data:
        return {'success': False, 'message': 'No data provided'}, 400

    title = (data.get('title') or '').strip()
    description = (data.get('description') or '').strip()
    geox = data.get('geox')
    geoy = data.get('geoy')

    if not title and not description:
        return {'success': False, 'message': 'No content to compare'}, 400

    combined_text = f"{title}. {description}" if title and description else (title or description)

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.report_id, r.public_key, r.title, r.description, 'General' AS category,
               r.status, l.x, l.y, CONCAT(l.x, ', ', l.y) AS locname
        FROM reports r
        JOIN location l ON r.location_id = l.location_id
        WHERE l.x IS NOT NULL AND l.y IS NOT NULL AND r.public_key IS NOT NULL
        ORDER BY r.created_at DESC
        LIMIT 100
    """)
    existing_reports = cursor.fetchall()
    con.close()

    duplicates = []

    for report in existing_reports:
        old_title = report.get('title') or ''
        old_desc = report.get('description') or ''
        old_text = f"{old_title}. {old_desc}" if old_title and old_desc else (old_title or old_desc)

        sim = text_similarity(combined_text, old_text)
        near, distance = coordinate_proximity(
            geox, geoy,
            report.get('x'), report.get('y')
        )

        if sim >= 0.80 or (sim >= 0.70 and near) or sim >= 0.90:
            duplicates.append({
                'report_id': report['report_id'],
                'public_key': report.get('public_key', ''),
                'title': old_title,
                'category': report.get('category', 'General'),
                'location': report.get('locname', ''),
                'similarity': sim,
                'distance_m': round(distance, 1) if near else None,
                'status': report.get('status', 'Pending')
            })

    duplicates.sort(key=lambda d: d['similarity'], reverse=True)
    duplicates = duplicates[:5]

    return {
        'success': True,
        'duplicates': duplicates,
        'has_duplicates': len(duplicates) > 0
    }


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session or session.get('user_role') != "admin":
        return redirect(url_for("login"))

    return redirect(url_for('activities'))


@app.route('/users', methods=['GET', 'POST'])
def users():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    # Updated for new ERD: accounts.contact_id -> contacts.contact_id
    cursor.execute(
        """
        SELECT
            a.account_id,
            CONCAT(a.first_name, ' ', a.last_name) AS fullname,
            a.middle_initial,
            '' AS profile_photo,
            c.email,
            c.phone_number,
            r.role,
            r.role_id,
            rep.user_id AS representative_user_id,
            rep.user_id AS usercreds_user_id
        FROM accounts a
        JOIN contacts c ON a.contact_id = c.contact_id
        JOIN usercreds u_rep_base ON u_rep_base.contact_id = c.contact_id
        JOIN (
            SELECT
                u.user_id,
                u.contact_id,
                ROW_NUMBER() OVER (
                    PARTITION BY u.contact_id
                    ORDER BY CASE WHEN u.emorph LIKE '%gmail.com' THEN 0 ELSE 1 END,
                             u.user_id ASC
                ) AS rn
            FROM usercreds u
        ) rep ON rep.user_id = u_rep_base.user_id AND rep.rn = 1
        JOIN user_role ur ON ur.user_id = rep.user_id
        JOIN role r ON r.role_id = ur.role_id
        ORDER BY a.account_id ASC
        """
    )
    rows = cursor.fetchall()
    
    

    if request.method == 'POST':
        cursor = con.cursor()
        acttype = request.form.get('act')
        account_id = request.form.get('account_id')

        if acttype == "change_role":
            target_user_id = request.form.get('usercreds_user_id')
            new_role_id = request.form.get('role_id')
            if target_user_id and new_role_id:
                cursor.execute("SELECT 1 FROM user_role WHERE user_id = %s", (target_user_id,))
                exists = cursor.fetchone()
                if exists:
                    cursor.execute("SELECT contact_id FROM usercreds WHERE user_id = %s", (target_user_id,))
                    c = cursor.fetchone()
                    if c:
                        cursor.execute("SELECT user_id FROM usercreds WHERE contact_id = %s", (c[0],))
                        us = cursor.fetchall()
                        for u_item in us:
                            cursor.execute("UPDATE user_role SET role_id = %s WHERE user_id = %s", (new_role_id, u_item[0]))
                else:
                    cursor.execute("INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)", (target_user_id, new_role_id))
                con.commit()
        elif account_id:
            if acttype == "remove":
                try:
                    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

                    # Get linked contact_id and address_id from accounts
                    cursor.execute("SELECT contact_id, address_id FROM accounts WHERE account_id = %s", (account_id,))
                    acc_row = cursor.fetchone()
                    c_id = acc_row[0] if acc_row else None
                    addr_id = acc_row[1] if acc_row else None

                    # 1. Delete activity_media and report_activity by this account
                    cursor.execute("""
                        DELETE am FROM activity_media am
                        JOIN report_activity ra ON am.activity_id = ra.activity_id
                        WHERE ra.account_id = %s
                    """, (account_id,))
                    cursor.execute("DELETE FROM report_activity WHERE account_id = %s", (account_id,))
                    cursor.execute("DELETE FROM announcements WHERE account_id = %s", (account_id,))

                    # 2. Delete user_role, access_attempt, credentials, usercreds, and contacts
                    if c_id:
                        cursor.execute("SELECT user_id FROM usercreds WHERE contact_id = %s", (c_id,))
                        users_list = cursor.fetchall()

                        for u_row in users_list:
                            u_id = u_row[0]
                            cursor.execute("""
                                DELETE aa FROM access_attempt aa
                                JOIN credentials cr ON aa.cred_id = cr.cred_id
                                WHERE cr.user_id = %s
                            """, (u_id,))
                            cursor.execute("DELETE FROM user_role WHERE user_id = %s", (u_id,))
                            cursor.execute("DELETE FROM credentials WHERE user_id = %s", (u_id,))
                            cursor.execute("DELETE FROM usercreds WHERE user_id = %s", (u_id,))

                        cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (c_id,))

                    # 3. Delete account and address
                    cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
                    if addr_id:
                        cursor.execute("DELETE FROM address WHERE address_id = %s", (addr_id,))

                    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
                    con.commit()
                except Exception as e:
                    print(f"Error removing account {account_id}: {e}")
                    con.rollback()
            else:
                lock_val = None
                ban_val = 0
                if acttype in ("ban", "restrict"):
                    lock_val = 'Y'
                    ban_val = 1
                elif acttype == "unban":
                    lock_val = 'N'
                    ban_val = 0

                if lock_val is not None:
                    update_sql = """
                        UPDATE credentials c
                        JOIN usercreds u ON u.user_id = c.user_id
                        JOIN accounts a ON a.contact_id = u.contact_id
                        SET c.is_locked = %s, c.is_banned = %s
                        WHERE a.account_id = %s
                    """
                    cursor.execute(update_sql, (lock_val, ban_val, account_id))
                    con.commit()

        con.close()
        return redirect(url_for("users"))

    cursor.execute("SELECT * FROM role")
    roles = cursor.fetchall()
    con.close()
    return render_template('users.html', users=rows, active_page='users', roles=roles)


@app.route('/activities')
def activities():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    q = (request.args.get('q') or '').strip()
    action_type = (request.args.get('action_type') or '').strip().lower()
    from_date = (request.args.get('from_date') or '').strip()
    to_date = (request.args.get('to_date') or '').strip()

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    activities_list = []

    def build_where(alias_dt_field: str, alias_title: str, alias_fullname: str, alias_type_literal: str, has_where: bool = False):
        clauses = []
        params = []

        if action_type:
            clauses.append(f"{alias_type_literal} = %s")
            params.append(action_type)

        if q:
            clauses.append(f"(LOWER({alias_title}) LIKE %s OR LOWER({alias_fullname}) LIKE %s)")
            needle = f"%{q.lower()}%"
            params.append(needle)
            params.append(needle)

        if from_date:
            clauses.append(f"DATE({alias_dt_field}) >= %s")
            params.append(from_date)

        if to_date:
            clauses.append(f"DATE({alias_dt_field}) <= %s")
            params.append(to_date)

        if not clauses:
            return "", []

        prefix = "AND " if has_where else "WHERE "
        return prefix + " AND ".join(clauses), params

    # 1) Reports created (type='report')
    where_report, params_report = build_where('r.created_at', 'r.title', "COALESCE(CONCAT(a.first_name, ' ', a.last_name), 'Resident')", "'report'", has_where=False)
    cursor.execute(
        f"""
        SELECT
            r.created_at AS dt,
            'report' AS type,
            r.title AS title,
            COALESCE(CONCAT(a.first_name, ' ', a.last_name), 'Resident') AS fullname,
            NULL AS text
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        {where_report}
        """,
        tuple(params_report)
    )
    activities_list.extend(cursor.fetchall())

    # 2) Report updates (type='report_update')
    where_update, params_update = build_where('COALESCE(r.last_activity, r.created_at)', 'r.title', "CONCAT(a.first_name, ' ', a.last_name)", "'report_update'", has_where=True)
    cursor.execute(
        f"""
        SELECT
            COALESCE(r.last_activity, r.created_at) AS dt,
            'update' AS type,
            r.title AS title,
            CONCAT(a.first_name, ' ', a.last_name) AS fullname,
            rp.content AS text
        FROM report_activity rp
        JOIN reports r ON rp.report_id = r.report_id
        JOIN accounts a ON rp.account_id = a.account_id
        WHERE rp.activity_type = 'report_update'
        {where_update}
        """,
        tuple(params_update)
    )
    activities_list.extend(cursor.fetchall())

    # 3) Feedback uploads (type='feedbacks' / 'feedback')
    where_feedback, params_feedback = build_where('COALESCE(r.last_activity, r.created_at)', 'r.title', "CONCAT(a.first_name, ' ', a.last_name)", "'feedback'", has_where=True)
    cursor.execute(
        f"""
        SELECT
            COALESCE(r.last_activity, r.created_at) AS dt,
            'feedback' AS type,
            r.title AS title,
            CONCAT(a.first_name, ' ', a.last_name) AS fullname,
            f.content AS text
        FROM report_activity f
        JOIN reports r ON f.report_id = r.report_id
        JOIN accounts a ON f.account_id = a.account_id
        WHERE f.activity_type IN ('feedbacks', 'feedback')
        {where_feedback}
        """,
        tuple(params_feedback)
    )
    activities_list.extend(cursor.fetchall())

    con.close()

    activities_list.sort(key=lambda x: x.get('dt') or datetime.min, reverse=True)

    for a in activities_list:
        dt = a.get('dt')
        a['dt'] = dt.strftime('%Y-%m-%d %H:%M:%S') if dt else ''

    return render_template('activities.html', activities=activities_list, active_page='activities')


# --- EXPORT ROUTES ---
@app.route('/api/export/users')
def export_users():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.account_id, CONCAT(a.first_name, " ", a.last_name) AS fullname, 
               c.email, c.phone_number, r.role 
        FROM accounts a
        JOIN contacts c ON a.contact_id = c.contact_id 
        JOIN usercreds u ON c.contact_id = u.contact_id
        JOIN user_role ur ON u.user_id = ur.user_id
        JOIN role r ON ur.role_id = r.role_id
        ORDER BY a.account_id ASC
    """)
    users_list = cursor.fetchall()
    con.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "User Accounts"

    headers = ["Account ID", "Full Name", "Email Address", "Phone Number", "Role"]
    ws.append(headers)

    header_fill = PatternFill(start_color="8B0000", end_color="8B0000", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    for i, u in enumerate(users_list, start=2):
        ws.cell(row=i, column=1, value=u['account_id'])
        ws.cell(row=i, column=2, value=u['fullname'])
        ws.cell(row=i, column=3, value=u['email'])
        ws.cell(row=i, column=4, value=u['phone_number'])
        ws.cell(row=i, column=5, value=u['role'])

        for col in range(1, 6):
            cell = ws.cell(row=i, column=col)
            cell.border = thin_border
            if col in [1, 5]:
                cell.alignment = Alignment(horizontal="center")

    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 35
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 15

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = f"ActBayan_Users_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    return send_file(output, as_attachment=True, download_name=filename, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.route('/api/export/activities')
def export_activities():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    q = (request.args.get('q') or '').strip()
    action_type = (request.args.get('action_type') or '').strip().lower()
    from_date = (request.args.get('from_date') or '').strip()
    to_date = (request.args.get('to_date') or '').strip()

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    activities_list = []

    def build_where(alias_dt_field, alias_title, alias_fullname, alias_type_literal, has_where=False):
        clauses = []
        params = []
        if action_type:
            clauses.append(f"{alias_type_literal} = %s")
            params.append(action_type)
        if q:
            clauses.append(f"(LOWER({alias_title}) LIKE %s OR LOWER({alias_fullname}) LIKE %s)")
            needle = f"%{q.lower()}%"
            params.extend([needle, needle])
        if from_date:
            clauses.append(f"DATE({alias_dt_field}) >= %s")
            params.append(from_date)
        if to_date:
            clauses.append(f"DATE({alias_dt_field}) <= %s")
            params.append(to_date)

        if not clauses:
            return "", []
        prefix = "AND " if has_where else "WHERE "
        return prefix + " AND ".join(clauses), params

    # Reports
    w_sql, w_params = build_where('r.created_at', 'r.title', 'COALESCE(CONCAT(a.first_name," ",a.last_name), "Resident")', "'report'", has_where=False)
    q1 = f"""
        SELECT r.created_at AS dt, 'Report' AS type, r.title,
               COALESCE(CONCAT(a.first_name,' ',a.last_name), 'Resident') AS fullname, '' AS text
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        {w_sql}
    """
    cursor.execute(q1, tuple(w_params))
    activities_list.extend(cursor.fetchall())

    # Feedbacks
    w_sql2, w_params2 = build_where('COALESCE(r.last_activity, r.created_at)', 'r.title', 'CONCAT(a.first_name," ",a.last_name)', "'feedback'", has_where=True)
    q2 = f"""
        SELECT COALESCE(r.last_activity, r.created_at) AS dt, 'Feedback' AS type, r.title,
               CONCAT(a.first_name,' ',a.last_name) AS fullname, f.content AS text
        FROM report_activity f
        LEFT JOIN reports r ON f.report_id = r.report_id
        LEFT JOIN accounts a ON f.account_id = a.account_id
        WHERE f.activity_type IN ('feedbacks', 'feedback')
        {w_sql2}
    """
    cursor.execute(q2, tuple(w_params2))
    activities_list.extend(cursor.fetchall())

    # Updates
    w_sql3, w_params3 = build_where('COALESCE(r.last_activity, r.created_at)', 'r.title', 'CONCAT(a.first_name," ",a.last_name)', "'report_update'", has_where=True)
    q3 = f"""
        SELECT COALESCE(r.last_activity, r.created_at) AS dt, 'Update' AS type, r.title,
               CONCAT(a.first_name,' ',a.last_name) AS fullname, rp.content AS text
        FROM report_activity rp
        LEFT JOIN reports r ON rp.report_id = r.report_id
        LEFT JOIN accounts a ON rp.account_id = a.account_id
        WHERE rp.activity_type = 'report_update'
        {w_sql3}
    """
    cursor.execute(q3, tuple(w_params3))
    activities_list.extend(cursor.fetchall())

    con.close()

    activities_list.sort(key=lambda x: x['dt'] if x['dt'] else datetime.min, reverse=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "User Activities"

    headers = ["Date & Time", "Action Type", "Title/Report", "Full Name", "Description"]
    ws.append(headers)

    header_fill = PatternFill(start_color="8B0000", end_color="8B0000", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    for i, act in enumerate(activities_list, start=2):
        dt_val = act['dt'].strftime('%Y-%m-%d %H:%M:%S') if act.get('dt') else ''
        ws.cell(row=i, column=1, value=dt_val)
        ws.cell(row=i, column=2, value=act.get('type', ''))
        ws.cell(row=i, column=3, value=act.get('title', ''))
        ws.cell(row=i, column=4, value=act.get('fullname', ''))
        ws.cell(row=i, column=5, value=act.get('text', ''))

        for col in range(1, 6):
            cell = ws.cell(row=i, column=col)
            cell.border = thin_border
            if col in [1, 2]:
                cell.alignment = Alignment(horizontal="center")
            else:
                cell.alignment = Alignment(horizontal="left", wrap_text=True if col == 5 else False)

    ws.column_dimensions['A'].width = 22
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 60

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = f"ActBayan_Activities_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    return send_file(output, as_attachment=True, download_name=filename, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.route('/api/comments/<int:report_id>')
def api_comments(report_id):
    con = connect_db()
    cursor = con.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            f.activity_id AS feedback_id,
            f.content AS comment_text,
            COALESCE(r.last_activity, r.created_at) AS uploaded_at,
            a.first_name,
            a.last_name
        FROM report_activity f
        LEFT JOIN reports r ON r.report_id = f.report_id
        LEFT JOIN accounts a ON a.account_id = f.account_id
        WHERE f.activity_type IN ('feedbacks', 'feedback') AND f.report_id = %s
        ORDER BY f.activity_id ASC
    """, (report_id,))
    comments = cursor.fetchall()
    con.close()

    for c in comments:
        if c.get('uploaded_at'):
            c['created_at_formatted'] = c['uploaded_at'].strftime('%b %d, %Y - %I:%M %p')
            del c['uploaded_at']
        else:
            c['created_at_formatted'] = ''

        c['reaction_counts'] = {}
        c['user_reaction'] = None

    return jsonify(comments)


@app.route('/api/react_comment', methods=['POST'])
def react_comment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.json or request.form
    feedback_id = data.get('feedback_id')
    reaction_type = data.get('reaction_type')

    if not feedback_id or not reaction_type:
        return jsonify({'success': False, 'message': 'Missing data'}), 400

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute(
        "SELECT activity_id FROM report_activity WHERE activity_type IN ('feedbacks', 'feedback') AND activity_id = %s",
        (feedback_id,)
    )
    row = cursor.fetchone()
    con.close()

    if not row:
        return jsonify({'success': False, 'message': 'Comment not found'}), 404

    return jsonify({'success': True, 'action': 'added', 'reaction': reaction_type})

@app.route("/api/getfullname/<int:account_id>")
def pulnem(account_id):
    con = connect_db()
    cursor = con.cursor()

    cursor.execute("""
        SELECT CONCAT_WS(' ', first_name, middle_initial, last_name) AS fulln
        FROM accounts
        WHERE account_id = %s
    """, (account_id,))

    result = cursor.fetchone()

    cursor.close()
    con.close()

    neym = result[0] if result else None

    if neym is None:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    return jsonify({'success': True, 'fullname': neym})    
    


@app.route('/api/report_updates/<int:report_id>')
def api_report_updates(report_id):
    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            rp.content AS update_text,
            am.path AS image_url,
            COALESCE(r.last_activity, r.created_at) AS submitted_at,
            rp.account_id
        FROM report_activity rp
        LEFT JOIN activity_media am ON am.activity_id = rp.activity_id
        LEFT JOIN reports r ON r.report_id = rp.report_id
        WHERE rp.activity_type = 'report_update' AND rp.report_id = %s
        ORDER BY rp.activity_id ASC
    """, (report_id,))
    updates = cursor.fetchall()
    con.close()

    for u in updates:
        if u.get('submitted_at'):
            u['created_at_formatted'] = u['submitted_at'].strftime('%B %d, %Y - %I:%M %p')
            del u['submitted_at']
        else:
            u['created_at_formatted'] = ''

    return jsonify(updates)


@app.route('/api/user_history/<int:account_id>')
def api_user_history(account_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    # Query 1: Login attempts (Formatted dates to prevent JSON serialization errors)
    cursor.execute(
        """
        SELECT 
            DATE_FORMAT(aa.attempted_at, '%b %d, %Y - %h:%i %p') AS attempted_at,
            aa.credential_used,
            aa.action AS status
        FROM access_attempt aa
        JOIN credentials c ON aa.cred_id = c.cred_id
        JOIN usercreds uc ON c.user_id = uc.user_id
        JOIN accounts a ON uc.contact_id = a.contact_id
        WHERE a.account_id = %s
        ORDER BY aa.attempted_at DESC
        LIMIT 100
        """,
        (account_id,)
    )
    logins = cursor.fetchall()

    # Query 2: Recent activities (Added r.title and formatted dates)
    cursor.execute(
        """
        SELECT 
            ra.activity_type,
            ra.content,
            COALESCE(r.title, 'General Update') AS report_title,
            DATE_FORMAT(COALESCE(r.last_activity, r.created_at), '%b %d, %Y - %h:%i %p') AS activity_time
        FROM report_activity ra
        LEFT JOIN reports r ON ra.report_id = r.report_id
        WHERE ra.account_id = %s
        ORDER BY ra.activity_id DESC
        LIMIT 100
        """,
        (account_id,)
    )
    activities = cursor.fetchall()

    con.close()
    
    # Handle potential None values from DATE_FORMAT if timestamps are missing
    for log in logins:
        if not log['attempted_at']:
            log['attempted_at'] = 'Unknown Date'
            
    for act in activities:
        if not act['activity_time']:
            act['activity_time'] = 'Unknown Date'

    return jsonify({'success': True, 'logins': logins, 'activities': activities})

@app.route('/admin/login_attempts')
def admin_login_attempts():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    # Updated for new ERD: access_attempt replaces login_logs
    cursor.execute("""
        SELECT
            attempt_id AS log_id,
            cred_id,
            credential_used AS emorph,
            action AS status,
            attempted_at AS attempt_time
        FROM access_attempt
        ORDER BY attempted_at DESC
    """)
    logs = cursor.fetchall()

    # Updated for new ERD: credentials + accounts.contact_id
    cursor.execute("""
        SELECT
            c.user_id,
            CASE WHEN c.last_failed_at IS NOT NULL THEN 1 ELSE 0 END AS failed_attempts,
            c.last_failed_at,
            c.is_locked,
            c.is_banned,
            c.ban_duration,
            c.lock_duration,
            a.first_name,
            a.last_name,
            '' AS profile_photo
        FROM credentials c
        JOIN usercreds u ON c.user_id = u.user_id
        JOIN contacts ct ON u.contact_id = ct.contact_id
        JOIN accounts a ON a.contact_id = ct.contact_id
        WHERE c.last_failed_at IS NOT NULL OR c.is_locked = 'Y' OR c.is_banned = 1
    """)
    banned_users = cursor.fetchall()

    con.close()
    return render_template('admin_login_attempts.html', logs=logs, banned_users=banned_users, active_page='login_attempts')


@app.route('/admin/reports')
def admin_reports():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            r.*,
            (SELECT rm.path FROM reports_media rm WHERE rm.report_id = r.report_id LIMIT 1) AS image_url,
            'General' AS category,
            a.first_name,
            a.last_name,
            '' AS reporter_photo,
            CONCAT(l.x, ', ', l.y) AS locname
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        LEFT JOIN location l ON r.location_id = l.location_id
        ORDER BY r.created_at DESC
    """)
    reports = cursor.fetchall()
    con.close()
    return render_template('admin_reports.html', reports=reports, active_page='reports')


@app.route('/')
def home():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    user_data = None
    if 'user_id' in session:
        try:
            cursor.execute(
                "SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s",
                (session['user_id'],)
            )
            rows = cursor.fetchall()
            if rows:
                user_data = rows[0]
        except Exception:
            pass

    reps = """
        SELECT
            r.title,
            (SELECT rm.path FROM reports_media rm WHERE rm.report_id = r.report_id LIMIT 1) AS image_url,
            r.description,
            r.status,
            'General' AS category
        FROM reports r
    """
    cursor.execute(reps)
    reports = cursor.fetchall()
    db.close()

    return render_template('index.html', user=user_data, reports=reports)


@app.route('/lgu', methods=['GET', 'POST'])
def lgu():
    if 'user_id' not in session or session.get('user_role') not in ('lgu', 'resident'):
        return redirect(url_for('logout'))

    account_id = session.get('user_id')

    sql_reps = """
        SELECT
            r.*,
            (SELECT rm.path FROM reports_media rm WHERE rm.report_id = r.report_id LIMIT 1) AS image_url,
            'General' AS category,
            COALESCE(a.first_name, 'Resident') AS first_name,
            COALESCE(a.last_name, '') AS last_name,
            '' AS profile_photo
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        ORDER BY r.created_at DESC
    """

    if request.method == 'POST':
        data = request.form
        report_id = data.get('report_id')
        description = data.get('update_description', '').strip()

        if not report_id or not description:
            return redirect(url_for('lgu'))

        image_url = None
        update_photo = request.files.get('update_photo')
        if update_photo and update_photo.filename:
            os.makedirs('static/uploads', exist_ok=True)
            filename = f"update_{report_id}_{int(datetime.now().timestamp())}_{secure_filename(update_photo.filename)}"
            filepath = f"static/uploads/{filename}"
            update_photo.save(filepath)
            image_url = filepath

        con = connect_db()
        cursor = con.cursor()

        # Updated for new ERD: insert into report_activity, then activity_media if photo exists
        query = """
            INSERT INTO report_activity (account_id, report_id, activity_type, content)
            VALUES (%s, %s, 'report_update', %s)
        """
        cursor.execute(query, (account_id, report_id, description))
        activity_id = cursor.lastrowid

        if image_url and activity_id:
            cursor.execute(
                "INSERT INTO activity_media (activity_id, path) VALUES (%s, %s)",
                (activity_id, image_url)
            )

        status = data.get('update_status')
        if status:
            cursor.execute(
                "UPDATE reports SET status = %s, last_activity = %s WHERE report_id = %s",
                (status, datetime.now(), report_id)
            )
        else:
            cursor.execute(
                "UPDATE reports SET last_activity = %s WHERE report_id = %s",
                (datetime.now(), report_id)
            )

        con.commit()
        con.close()
        return redirect(url_for('lgu'))

    # GET
    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql_reps)
    reps = cursor.fetchall()

    media_by_report = {}
    try:
        _lgu_ids = [r.get('report_id') for r in reps if r.get('report_id') is not None]
        if _lgu_ids:
            _lgu_ph = ",".join(["%s"] * len(_lgu_ids))
            cursor.execute(
                f"SELECT report_id, path FROM reports_media WHERE report_id IN ({_lgu_ph}) ORDER BY report_id",
                tuple(_lgu_ids)
            )
            for mrow in cursor.fetchall():
                media_by_report.setdefault(mrow.get('report_id'), []).append(mrow.get('path'))
    except Exception:
        media_by_report = {}

    report_ids = [r.get('report_id') for r in reps if r.get('report_id') is not None]

    # ===== FEEDBACKS / COMMENTS =====
    feedbacks_by_report = {}
    feedback_counts_by_report = {}

    if report_ids:
        placeholders = ','.join(['%s'] * len(report_ids))
        feedback_query = f"""
            SELECT
                f.activity_id AS feedback_id,
                f.report_id,
                f.account_id,
                f.content AS feedback,
                COALESCE(r.last_activity, r.created_at) AS uploaded_at,
                '' AS profile_photo,
                CONCAT(a.first_name, ' ', a.last_name) AS fullname
            FROM report_activity f
            LEFT JOIN reports r ON r.report_id = f.report_id
            LEFT JOIN accounts a ON a.account_id = f.account_id
            WHERE f.activity_type IN ('feedbacks', 'feedback') AND f.report_id IN ({placeholders})
            ORDER BY f.activity_id DESC
        """
        cursor.execute(feedback_query, tuple(report_ids))
        all_feedbacks = cursor.fetchall()
        now = datetime.now()
        for fb in all_feedbacks:
            if fb.get('uploaded_at'):
                diff = now - fb['uploaded_at']
                if diff.days > 7:
                    fb['time_ago'] = fb['uploaded_at'].strftime('%b %d, %Y')
                elif diff.days > 0:
                    fb['time_ago'] = f"{diff.days}d ago"
                else:
                    seconds = diff.seconds
                    if seconds >= 3600:
                        fb['time_ago'] = f"{seconds // 3600}h ago"
                    elif seconds >= 60:
                        fb['time_ago'] = f"{seconds // 60}m ago"
                    else:
                        fb['time_ago'] = "Just now"
            else:
                fb['time_ago'] = ""
            feedbacks_by_report.setdefault(fb.get('report_id'), []).append(fb)

    for rid, fbs in feedbacks_by_report.items():
        feedback_counts_by_report[rid] = len(fbs)

    # ===== UPVOTES (from reports.upvote_count INT column) =====
    upvote_counts = {r['report_id']: int(r.get('upvote_count') or 0) for r in reps if r.get('report_id') is not None}
    user_upvoted = set()

    if report_ids and account_id:
        placeholders = ','.join(['%s'] * len(report_ids))
        cursor.execute(
            f"""
            SELECT report_id FROM report_activity
            WHERE account_id = %s AND activity_type = 'upvote' AND report_id IN ({placeholders})
            """,
            (account_id,) + tuple(report_ids)
        )
        for row in cursor.fetchall():
            user_upvoted.add(row['report_id'])

    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s",
        (account_id,)
    )
    user_data = cursor.fetchone()
    con.close()

    return render_template(
        "lgu.html",
        reps=reps,
        media_by_report=media_by_report,
        feedbacks_by_report=feedbacks_by_report,
        feedback_counts_by_report=feedback_counts_by_report,
        upvote_counts=upvote_counts,
        user_upvoted=user_upvoted,
        user=user_data
    )

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    account_id = session.get('user_id')
    con = connect_db()
    cursor = con.cursor(dictionary=True)

    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo, 'Verified' AS account_status FROM accounts WHERE account_id = %s",
        (account_id,)
    )
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    # Find reports created by the logged-in user to prioritize/tag them
    cursor.execute("""
        SELECT DISTINCT report_id
        FROM report_activity
        WHERE account_id = %s AND activity_type = 'report_created'
    """, (account_id,))
    my_report_ids = {row['report_id'] for row in cursor.fetchall()}

    notifications_list = []
    now = datetime.now()

    def format_time_ago(dt_val):
        if not dt_val:
            return "Recently"
        diff = now - dt_val
        if diff.days > 7:
            return dt_val.strftime('%b %d, %Y')
        elif diff.days > 0:
            return f"{diff.days}d ago"
        else:
            seconds = max(0, int(diff.total_seconds()))
            if seconds >= 3600:
                return f"{seconds // 3600}h ago"
            elif seconds >= 60:
                return f"{seconds // 60}m ago"
            return "Just now"

    # 1. LGU Progress Updates on Reports (activity_type = 'report_update')
    cursor.execute("""
        SELECT
            rp.activity_id,
            rp.report_id,
            rp.content AS update_text,
            r.title AS report_title,
            r.status,
            r.public_key,
            COALESCE(r.last_activity, r.created_at) AS dt,
            l.x,
            l.y,
            CONCAT(l.x, ', ', l.y) AS locname
        FROM report_activity rp
        JOIN reports r ON rp.report_id = r.report_id
        LEFT JOIN location l ON r.location_id = l.location_id
        WHERE rp.activity_type = 'report_update'
        ORDER BY rp.activity_id DESC
        LIMIT 30
    """)
    for row in cursor.fetchall():
        dt_val = row.get('dt')
        is_mine = row['report_id'] in my_report_ids
        has_coords = row.get('x') is not None and row.get('y') is not None
        notifications_list.append({
            'id': f"upd_{row['activity_id']}",
            'type': 'concern_update',
            'category_label': 'Your Report Update' if is_mine else 'LGU Status Update',
            'icon': 'fa-clipboard-check',
            'color': 'blue',
            'title': f"LGU updated \"{row['report_title']}\"",
            'message': (row['update_text'][:140] + '...') if row.get('update_text') and len(row['update_text']) > 140 else (row.get('update_text') or f"Status is now {row.get('status', 'Pending')}."),
            'status': row.get('status') or 'Pending',
            'report_id': row['report_id'],
            'public_key': row.get('public_key') or '',
            'has_coords': has_coords,
            'locname': row.get('locname') or 'Barangay GMN',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    # 2. Community Comments & Upvotes (activity_type IN ('feedback', 'feedbacks', 'upvote'))
    cursor.execute("""
        SELECT
            ra.activity_id,
            ra.report_id,
            ra.account_id,
            ra.activity_type,
            ra.content,
            r.title AS report_title,
            r.status,
            r.public_key,
            COALESCE(r.last_activity, r.created_at) AS dt,
            COALESCE(CONCAT(a.first_name, ' ', a.last_name), 'A resident') AS actor_name,
            l.x,
            l.y,
            CONCAT(l.x, ', ', l.y) AS locname
        FROM report_activity ra
        JOIN reports r ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        LEFT JOIN location l ON r.location_id = l.location_id
        WHERE ra.activity_type IN ('feedback', 'feedbacks', 'upvote')
        ORDER BY ra.activity_id DESC
        LIMIT 30
    """)
    for row in cursor.fetchall():
        dt_val = row.get('dt')
        act_type = row.get('activity_type')
        actor = row.get('actor_name', 'A resident').strip() or 'A resident'
        has_coords = row.get('x') is not None and row.get('y') is not None
        if act_type == 'upvote':
            notif_title = f"{actor} upvoted \"{row['report_title']}\""
            notif_msg = "Community support increased on this concern."
            icon = 'fa-arrow-up'
            color = 'orange'
            cat_lbl = 'Community Upvote'
        else:
            notif_title = f"{actor} commented on \"{row['report_title']}\""
            notif_msg = (row['content'][:140] + '...') if row.get('content') and len(row['content']) > 140 else (row.get('content') or '')
            icon = 'fa-comment-dots'
            color = 'green'
            cat_lbl = 'New Comment'

        notifications_list.append({
            'id': f"act_{row['activity_id']}",
            'type': 'concern_update',
            'category_label': cat_lbl,
            'icon': icon,
            'color': color,
            'title': notif_title,
            'message': notif_msg,
            'status': row.get('status') or 'Pending',
            'report_id': row['report_id'],
            'public_key': row.get('public_key') or '',
            'has_coords': has_coords,
            'locname': row.get('locname') or 'Barangay GMN',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    # 3. Official Announcements
    cursor.execute("""
        SELECT a.ann_id, a.ann_title, a.ann_desc, a.category, a.submitted_at,
               acc.first_name, acc.last_name
        FROM announcements a
        LEFT JOIN accounts acc ON a.account_id = acc.account_id
        ORDER BY a.submitted_at DESC
        LIMIT 20
    """)
    for row in cursor.fetchall():
        dt_val = row.get('submitted_at')
        cat = row.get('category') or 'General'
        desc = row.get('ann_desc') or ''
        notifications_list.append({
            'id': f"ann_{row['ann_id']}",
            'type': 'announcement',
            'category_label': f"Announcement • {cat}",
            'icon': 'fa-bullhorn',
            'color': 'red',
            'title': row.get('ann_title') or 'Official Barangay Announcement',
            'message': (desc[:140] + '...') if len(desc) > 140 else desc,
            'ann_id': row['ann_id'],
            'ann_title': row.get('ann_title') or '',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    # 4. Mapped Community Reports / Area Alerts
    cursor.execute("""
        SELECT
            r.report_id,
            r.title,
            r.description,
            r.status,
            r.public_key,
            r.created_at AS dt,
            l.x,
            l.y,
            CONCAT(l.x, ', ', l.y) AS locname,
            COALESCE(CONCAT(a.first_name, ' ', a.last_name), 'Resident') AS reporter_name
        FROM reports r
        JOIN location l ON r.location_id = l.location_id
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        WHERE l.x IS NOT NULL AND l.y IS NOT NULL
        ORDER BY r.created_at DESC
        LIMIT 25
    """)
    for row in cursor.fetchall():
        dt_val = row.get('dt')
        desc = row.get('description') or ''
        notifications_list.append({
            'id': f"map_{row['report_id']}",
            'type': 'map_alert',
            'category_label': 'Map Pin Alert',
            'icon': 'fa-map-marker-alt',
            'color': 'purple',
            'title': f"Pinned Concern: \"{row['title']}\"",
            'message': (desc[:130] + '...') if len(desc) > 130 else (desc or f"Reported by {row.get('reporter_name')} at {row.get('locname')}"),
            'status': row.get('status') or 'Pending',
            'report_id': row['report_id'],
            'public_key': row.get('public_key') or '',
            'has_coords': True,
            'locname': row.get('locname') or '',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    con.close()

    # Sort all notifications newest first
    notifications_list.sort(key=lambda x: x.get('timestamp') or '', reverse=True)

    return render_template(
        'notifications.html',
        user=user_data,
        notifications=notifications_list,
        notifications_json=json.dumps(notifications_list)
    )

@app.route('/lgu_notifications')
def lgu_notifications():
    if 'user_id' not in session or session.get('user_role') not in ('lgu', 'resident'):
        return redirect(url_for('logout'))

    account_id = session.get('user_id')
    con = connect_db()
    cursor = con.cursor(dictionary=True)

    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo, 'Verified' AS account_status FROM accounts WHERE account_id = %s",
        (account_id,)
    )
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    # Find reports created by the logged-in user to prioritize/tag them
    cursor.execute("""
        SELECT DISTINCT report_id
        FROM report_activity
        WHERE account_id = %s AND activity_type = 'report_created'
    """, (account_id,))
    my_report_ids = {row['report_id'] for row in cursor.fetchall()}

    notifications_list = []
    now = datetime.now()

    def format_time_ago(dt_val):
        if not dt_val:
            return "Recently"
        diff = now - dt_val
        if diff.days > 7:
            return dt_val.strftime('%b %d, %Y')
        elif diff.days > 0:
            return f"{diff.days}d ago"
        else:
            seconds = max(0, int(diff.total_seconds()))
            if seconds >= 3600:
                return f"{seconds // 3600}h ago"
            elif seconds >= 60:
                return f"{seconds // 60}m ago"
            return "Just now"

    # 1. LGU Progress Updates on Reports (activity_type = 'report_update')
    cursor.execute("""
        SELECT
            rp.activity_id,
            rp.report_id,
            rp.content AS update_text,
            r.title AS report_title,
            r.status,
            r.public_key,
            COALESCE(r.last_activity, r.created_at) AS dt,
            l.x,
            l.y,
            CONCAT(l.x, ', ', l.y) AS locname
        FROM report_activity rp
        JOIN reports r ON rp.report_id = r.report_id
        LEFT JOIN location l ON r.location_id = l.location_id
        WHERE rp.activity_type = 'report_update'
        ORDER BY rp.activity_id DESC
        LIMIT 30
    """)
    for row in cursor.fetchall():
        dt_val = row.get('dt')
        is_mine = row['report_id'] in my_report_ids
        has_coords = row.get('x') is not None and row.get('y') is not None
        notifications_list.append({
            'id': f"upd_{row['activity_id']}",
            'type': 'concern_update',
            'category_label': 'Your Report Update' if is_mine else 'LGU Status Update',
            'icon': 'fa-clipboard-check',
            'color': 'blue',
            'title': f"LGU updated \"{row['report_title']}\"",
            'message': (row['update_text'][:140] + '...') if row.get('update_text') and len(row['update_text']) > 140 else (row.get('update_text') or f"Status is now {row.get('status', 'Pending')}."),
            'status': row.get('status') or 'Pending',
            'report_id': row['report_id'],
            'public_key': row.get('public_key') or '',
            'has_coords': has_coords,
            'locname': row.get('locname') or 'Barangay GMN',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    # 2. Community Comments & Upvotes (activity_type IN ('feedback', 'feedbacks', 'upvote'))
    cursor.execute("""
        SELECT
            ra.activity_id,
            ra.report_id,
            ra.content AS comment_text,
            ra.activity_type,
            COALESCE(r.last_activity, r.created_at) AS dt,
            CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
            r.title AS report_title
        FROM report_activity ra
        JOIN reports r ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        WHERE ra.activity_type IN ('feedback', 'feedbacks', 'upvote')
        ORDER BY ra.activity_id DESC
        LIMIT 40
    """)
    for row in cursor.fetchall():
        dt_val = row.get('dt')
        act = row.get('activity_type') or ''
        notifications_list.append({
            'id': f"act_{row['activity_id']}",
            'type': 'concern_update',
            'category_label': 'New Upvote' if act == 'upvote' else 'New Comment',
            'icon': 'fa-thumbs-up' if act == 'upvote' else 'fa-comment',
            'color': 'green' if act == 'upvote' else 'orange',
            'title': f"{row.get('actor_name') or 'A user'} { 'upvoted' if act == 'upvote' else 'commented on' } \"{row.get('report_title') or 'a concern'}\"",
            'message': (row.get('comment_text') or '')[:140],
            'status': '',
            'report_id': row['report_id'],
            'public_key': '',
            'has_coords': False,
            'locname': '',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    # 3. Official Announcements
    cursor.execute("""
        SELECT a.ann_id, a.ann_title, a.ann_desc, a.category, a.submitted_at,
               acc.first_name, acc.last_name
        FROM announcements a
        LEFT JOIN accounts acc ON a.account_id = acc.account_id
        ORDER BY a.submitted_at DESC
        LIMIT 20
    """)
    for row in cursor.fetchall():
        dt_val = row.get('submitted_at')
        cat = row.get('category') or 'General'
        desc = row.get('ann_desc') or ''
        notifications_list.append({
            'id': f"ann_{row['ann_id']}",
            'type': 'announcement',
            'category_label': f"Announcement • {cat}",
            'icon': 'fa-bullhorn',
            'color': 'red',
            'title': row.get('ann_title') or 'Official Barangay Announcement',
            'message': (desc[:140] + '...') if len(desc) > 140 else desc,
            'ann_id': row['ann_id'],
            'ann_title': row.get('ann_title') or '',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    # 4. Mapped Community Reports / Area Alerts
    cursor.execute("""
        SELECT
            r.report_id,
            r.title,
            r.description,
            r.status,
            r.public_key,
            r.created_at AS dt,
            l.x,
            l.y,
            CONCAT(l.x, ', ', l.y) AS locname,
            COALESCE(CONCAT(a.first_name, ' ', a.last_name), 'Resident') AS reporter_name
        FROM reports r
        JOIN location l ON r.location_id = l.location_id
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        WHERE l.x IS NOT NULL AND l.y IS NOT NULL
        ORDER BY r.created_at DESC
        LIMIT 25
    """)
    for row in cursor.fetchall():
        dt_val = row.get('dt')
        desc = row.get('description') or ''
        notifications_list.append({
            'id': f"map_{row['report_id']}",
            'type': 'map_alert',
            'category_label': 'Map Pin Alert',
            'icon': 'fa-map-marker-alt',
            'color': 'purple',
            'title': f"Pinned Concern: \"{row['title']}\"",
            'message': (desc[:130] + '...') if len(desc) > 130 else (desc or f"Reported by {row.get('reporter_name')} at {row.get('locname')}"),
            'status': row.get('status') or 'Pending',
            'report_id': row['report_id'],
            'public_key': row.get('public_key') or '',
            'has_coords': True,
            'locname': row.get('locname') or '',
            'time_ago': format_time_ago(dt_val),
            'timestamp': dt_val.strftime('%Y-%m-%d %H:%M:%S') if dt_val else ''
        })

    con.close()

    # Sort all notifications newest first
    notifications_list.sort(key=lambda x: x.get('timestamp') or '', reverse=True)

    return render_template(
        'lgu_notif.html',
        user=user_data,
        notifications=notifications_list,
        notifications_json=json.dumps(notifications_list)
    )

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    account_id = session.get('user_id')
    user_name = session.get('user_name')

    sql_recent = """
        SELECT
            r.*,
            (SELECT rm.path FROM reports_media rm WHERE rm.report_id = r.report_id LIMIT 1) AS image_url,
            'General' AS category,
            COALESCE(a.first_name, 'Resident') AS first_name,
            COALESCE(a.last_name, '') AS last_name
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        ORDER BY r.created_at DESC
    """
    cursor.execute(sql_recent)
    all_concerns = cursor.fetchall()

    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo, 'Verified' AS account_status FROM accounts WHERE account_id = %s",
        (account_id,)
    )
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    cursor.execute("SELECT * FROM announcements ORDER BY submitted_at DESC LIMIT 1")
    ann_rows = cursor.fetchall()
    latest_ann = ann_rows[0] if ann_rows else None
    if latest_ann and latest_ann['submitted_at']:
        latest_ann['formatted_date'] = latest_ann['submitted_at'].strftime('%b %d, %Y')

    con.close()

    return render_template(
        'dashboard.html',
        recent=all_concerns,
        ngalan=user_name,
        user=user_data,
        latest_ann=latest_ann
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    con = connect_db()
    cursor = con.cursor(buffered=True)

    if request.method == 'POST':
        data = request.form
        u = data.get('e', '').strip()
        p = data.get('pass', '').strip()

        if not u or not p:
            con.close()
            return render_template('login.html', error="Please enter email/phone and password")

        u = u.replace(' ', '')
        if u.startswith('+63'):
            u = '0' + u[3:]

        # 1. Check registration table (updated to password_hash)
        query_reg = "SELECT registration_id, email_address, phone_number, password_hash FROM registration WHERE email_address = %s OR phone_number = %s"
        cursor.execute(query_reg, (u, u))
        reg_record = cursor.fetchone()

        if reg_record and check_password_bcrypt(reg_record[3], p):
            reg_id = reg_record[0]
            if reg_id:
                session['reg_id'] = reg_id
                con.close()
                return redirect(url_for('cd'))

        # 2. Check credentials + password_hash
        credquery = """
            SELECT u.emorph, p.password_hash, c.cred_id
            FROM credentials AS c
            JOIN usercreds AS u ON u.user_id = c.user_id
            JOIN password AS p ON p.pass_id = c.pass_id
            WHERE u.emorph = %s
        """
        cursor.execute(credquery, (u,))
        creds = cursor.fetchone()
        cred_id_val = creds[2] if creds else None

        if creds and check_password_bcrypt(creds[1], p):
            emorph = creds[0]

            # Updated for new ERD: accounts.contact_id = contacts.contact_id
            neym = """
                SELECT a.account_id, a.first_name
                FROM accounts a
                JOIN contacts c ON a.contact_id = c.contact_id
                WHERE c.email = %s OR c.phone_number = %s
            """
            cursor.execute(neym, (emorph, emorph))
            nem = cursor.fetchone()

            if nem:
                account_id = nem[0]
                pangalan = nem[1]

                rowl = """
                    SELECT u.user_id, u.emorph, r.role
                    FROM usercreds u
                    JOIN contacts c ON u.contact_id = c.contact_id
                    JOIN user_role ur ON u.user_id = ur.user_id
                    JOIN role r ON ur.role_id = r.role_id
                    WHERE u.emorph = %s
                """
                cursor.execute(rowl, (emorph,))
                rul = cursor.fetchone()

                usercreds_user_id = None
                role_value = ""
                if rul:
                    usercreds_user_id = rul[0]
                    if len(rul) > 2 and rul[2] is not None:
                        role_value = str(rul[2]).strip().casefold()

                if usercreds_user_id is not None:
                    ban_check_sql = "SELECT is_locked, is_banned, ban_duration, lock_duration FROM credentials WHERE user_id = %s"
                    cursor.execute(ban_check_sql, (usercreds_user_id,))
                    ban_row = cursor.fetchone()
                    is_locked = ban_row[0] if ban_row else None
                    is_banned = ban_row[1] if ban_row else 0
                    lock_duration = ban_row[3] if ban_row and len(ban_row) > 3 else None

                    ban_reason = None
                    if is_locked == 'Y' or is_banned == 1:
                        ban_reason = "This account is banned."
                    elif lock_duration is not None and str(lock_duration).strip() not in ('', '0', 'None', 'N'):
                        ban_reason = "Temporarily banned for profanity. Try again later."

                    if ban_reason:
                        cursor.execute(
                            "INSERT INTO access_attempt (cred_id, credential_used, attempted_at, action) VALUES (%s, %s, %s, %s)",
                            (cred_id_val, u, datetime.now(), 'Failed (Banned)')
                        )
                        con.commit()
                        con.close()
                        return render_template('login.html', error=ban_reason)

                # Log successful login into access_attempt and update credentials
                cursor.execute(
                    "INSERT INTO access_attempt (cred_id, credential_used, attempted_at, action) VALUES (%s, %s, %s, %s)",
                    (cred_id_val, u, datetime.now(), 'Success')
                )
                log_id = cursor.lastrowid
                if cred_id_val:
                    cursor.execute(
                        "UPDATE credentials SET is_active = 1, last_active_on = %s WHERE cred_id = %s",
                        (datetime.now(), cred_id_val)
                    )
                con.commit()

                session['user_id'] = account_id
                session['user_name'] = pangalan
                session['emorph'] = u
                session['log_id'] = log_id
                session['cred_id'] = cred_id_val

                if role_value == 'lgu official':
                    session['user_role'] = 'lgu'
                    con.close()
                    return redirect(url_for("lgu"))
                elif role_value == "admin":
                    session['user_role'] = 'admin'
                    con.close()
                    return redirect(url_for("admin"))

                session['user_role'] = 'resident'
                con.close()
                return redirect(url_for("barangay_map"))

        # Log failed login into access_attempt and update credentials.last_failed_at
        cursor.execute(
            "INSERT INTO access_attempt (cred_id, credential_used, attempted_at, action) VALUES (%s, %s, %s, %s)",
            (cred_id_val, u, datetime.now(), 'Failed')
        )
        if cred_id_val:
            cursor.execute(
                "UPDATE credentials SET last_failed_at = %s WHERE cred_id = %s",
                (datetime.now(), cred_id_val)
            )
        con.commit()
        con.close()
        return render_template('login.html', error="Invalid credentials")

    con.close()
    return render_template('login.html')


@app.route('/file_concern', methods=['GET', 'POST'])
def file_concern():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    if request.method == 'POST':
        con.autocommit = False
        data = request.form
        fn = request.form.get("fn")

        title = data.get('title')
        description = data.get('description')
        locname = data.get('location') or ''

        geox = data.get('geox')
        geoy = data.get('geoy')
        if geox is None or str(geox).strip() == '':
            geox = 0
        if geoy is None or str(geoy).strip() == '':
            geoy = 0

        cursor.execute("SELECT account_id FROM accounts WHERE account_id = %s", (session['user_id'],))
        user_rows = cursor.fetchall()
        user_record = user_rows[0] if user_rows else None

        if not user_record:
            con.close()
            return redirect(url_for('login'))

        account_id = user_record['account_id']

        ALLOWED_IMG_EXTS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg', 'tif', 'tiff', 'ico', 'heic', 'heif'}
        ALLOWED_VIDEO_EXTS = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', '3gp',
                              '3g2', 'ogv', 'ogg', 'mts', 'm2ts', 'ts', 'mxf', 'vob', 'rm',
                              'rmvb', 'asf', 'f4v', 'mpg', 'mpeg', 'mpe', 'm1v', 'm2v'}
        ALLOWED_EXTS = ALLOWED_IMG_EXTS | ALLOWED_VIDEO_EXTS
        MAX_FILES = 5

        def _ext_ok(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS

        files = request.files.getlist('concern_photos')
        if not files or all(not (f and f.filename) for f in files):
            legacy = request.files.get('concern_photo')
            files = [legacy] if legacy and legacy.filename else []

        saved_paths = []
        if files:
            os.makedirs('static/uploads/concerns', exist_ok=True)
            ts = int(datetime.now().timestamp())
            for i, f in enumerate(files[:MAX_FILES]):
                if not f or not f.filename or not _ext_ok(f.filename):
                    continue
                safe_name = secure_filename(f.filename)
                filename = f"concern_{account_id}_{ts}_{i}_{safe_name}"
                filepath = f"static/uploads/concerns/{filename}"
                f.save(filepath)
                saved_paths.append(filepath)

        # For fn == "pc" (posting feedback)
        if fn == "pc":
            feedback = (data.get('comment') or '').strip()
            report_id = data.get('report_id')

            from profanity import check_profanity as _check_profanity
            is_profane, matched_word = _check_profanity(feedback)
            wants_json = (
                request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                or 'application/json' in (request.headers.get('Accept') or '')
                or request.args.get('format') == 'json'
            )
            if is_profane:
                now = datetime.now()
                try:
                    strikes = int(session.get('profanity_strikes', 0) or 0)
                except Exception:
                    strikes = 0
                first_ts_raw = session.get('profanity_first_at')
                first_ts = None
                if first_ts_raw:
                    try:
                        first_ts = datetime.fromisoformat(str(first_ts_raw))
                    except Exception:
                        first_ts = None
                if not first_ts or (now - first_ts) > timedelta(minutes=2):
                    strikes = 0
                    first_ts = now
                    session['profanity_first_at'] = now.isoformat()
                strikes += 1
                session['profanity_strikes'] = strikes
                con.rollback()

                try:
                    window_left = max(0, int((timedelta(minutes=2) - (now - first_ts)).total_seconds()))
                except Exception:
                    window_left = 120

                if strikes == 1:
                    warn_msg = "Hey! Don't you dare. Watch your words! (1/3)"
                elif strikes == 2:
                    warn_msg = f"You trying again huh? Last warning! (2/3, {window_left}s left)"
                else:
                    warn_msg = None

                if strikes >= 3:
                    try:
                        cursor.execute("""
                            UPDATE credentials c
                            JOIN usercreds uc ON c.user_id = uc.user_id
                            JOIN accounts a ON a.contact_id = uc.contact_id
                            SET c.is_banned = 1, c.ban_duration = 5, c.lock_duration = 5
                            WHERE a.account_id = %s
                        """, (account_id,))
                        con.commit()
                    except Exception as e:
                        print(f"Profanity ban failed: {e}")
                        con.rollback()
                    session['profanity_strikes'] = 0
                    session.pop('profanity_first_at', None)
                    con.close()
                    ban_msg = 'Banned for 5 minutes: 3x profanity in 2 minutes. Time-out for you!'
                    if wants_json:
                        return jsonify({
                            'success': False,
                            'blocked': True,
                            'banned': True,
                            'strikes': 3,
                            'window': '2min',
                            'message': ban_msg
                        }), 403
                    flash(ban_msg, 'error')
                    return redirect(url_for('file_concern'))

                con.close()
                if wants_json:
                    return jsonify({
                        'success': False,
                        'blocked': True,
                        'banned': False,
                        'strikes': strikes,
                        'matched': matched_word,
                        'message': warn_msg
                    }), 400
                flash(warn_msg, 'error')
                return redirect(url_for('file_concern'))

            if report_id and feedback:
                # Updated for new ERD: insert into report_activity with 'feedbacks'
                comque = """
                    INSERT INTO report_activity (account_id, report_id, activity_type, content)
                    VALUES (%s, %s, 'feedbacks', %s)
                """
                cursor.execute(comque, (account_id, report_id, feedback))
                cursor.execute(
                    "UPDATE reports SET last_activity = %s WHERE report_id = %s",
                    (datetime.now(), report_id)
                )

                if wants_json:
                    con.commit()
                    con.close()
                    return jsonify({'success': True, 'message': 'Comment sent successfully!'})

        else:
            # 1. Insert coordinates + location name into location (x, y, locname)
            cursor.execute("INSERT INTO location (x, y, locname) VALUES (%s, %s, %s)", (geox, geoy, locname))
            location_id = cursor.lastrowid

            # 2. Insert report into reports (new ERD schema)
            public_key = str(uuid.uuid4())
            now_ts = datetime.now()
            cursor.execute("""
                INSERT INTO reports (title, location_id, description, status, created_at, last_activity, public_key, upvote_count)
                VALUES (%s, %s, %s, 'Pending', %s, %s, %s, 0)
            """, (title, location_id, description, now_ts, now_ts, public_key))
            report_id = cursor.lastrowid

            # 3. Record report creator in report_activity
            cursor.execute("""
                INSERT INTO report_activity (account_id, report_id, activity_type, content)
                VALUES (%s, %s, 'report_created', %s)
            """, (account_id, report_id, title))

            # 4. Store all media paths in reports_media
            if saved_paths:
                cursor.executemany(
                    "INSERT INTO reports_media (report_id, path) VALUES (%s, %s)",
                    [(report_id, p) for p in saved_paths]
                )

        con.commit()
        con.close()
        return redirect(url_for('file_concern'))

    # GET
    session_user_id = session.get('user_id')

    # 1. Reports owned by the logged-in user (via report_activity 'report_created')
    cursor.execute("""
        SELECT r.report_id, r.title, r.description, r.status, r.created_at, r.last_activity,
               r.public_key, r.upvote_count, r.location_id,
               a.first_name, a.last_name, '' AS profile_photo,
               'owner' AS user_relation,
               '' AS image_url, '' AS category, '' AS location
        FROM reports r
        JOIN report_activity ra ON r.report_id = ra.report_id
            AND ra.activity_type = 'report_created'
        JOIN accounts a ON ra.account_id = a.account_id
        WHERE ra.account_id = %s
    """, (session_user_id,))
    own_concerns = cursor.fetchall()

    # 2. Reports upvoted by the logged-in user (via report_activity 'upvote')
    cursor.execute("""
        SELECT r.report_id, r.title, r.description, r.status, r.created_at, r.last_activity,
               r.public_key, r.upvote_count, r.location_id,
               a.first_name, a.last_name, '' AS profile_photo,
               'upvoted' AS user_relation,
               '' AS image_url, '' AS category, '' AS location
        FROM reports r
        JOIN report_activity ra ON r.report_id = ra.report_id
            AND ra.activity_type = 'upvote'
        JOIN accounts a ON ra.account_id = a.account_id
        WHERE ra.account_id = %s
    """, (session_user_id,))
    upvoted_concerns = cursor.fetchall()

    # Combine owned + upvoted, deduplicate by report_id (owned takes priority)
    seen_ids = set()
    all_concerns = []
    for c in own_concerns + upvoted_concerns:
        rid = c.get('report_id')
        if rid not in seen_ids:
            seen_ids.add(rid)
            all_concerns.append(c)

    # Sort newest first
    all_concerns.sort(key=lambda c: c.get('created_at') or '', reverse=True)

    # Load extra media (2nd..Nth files) grouped by report for cover + "+N" badge.
    # Wrapped in try/except so page still renders if reports_media is missing.
    media_by_report = {}
    media_counts_by_report = {}
    try:
        _rep_ids = [c.get('report_id') for c in all_concerns if c.get('report_id') is not None]
        if _rep_ids:
            _ph = ",".join(["%s"] * len(_rep_ids))
            cursor.execute(
                f"SELECT report_id, path FROM reports_media WHERE report_id IN ({_ph}) ORDER BY report_id",
                tuple(_rep_ids)
            )
            for mrow in cursor.fetchall():
                rid = mrow.get('report_id')
                media_by_report.setdefault(rid, []).append(mrow.get('path'))
            for rid, plist in media_by_report.items():
                media_counts_by_report[rid] = len(plist)
    except Exception:
        media_by_report = {}
        media_counts_by_report = {}

    # Attach cover image_url to each concern (first media path from reports_media)
    for c in all_concerns:
        plist = media_by_report.get(c.get('report_id'), [])
        c['image_url'] = plist[0] if plist else ''

    cursor.execute("""
        SELECT
            rp.activity_id,
            rp.report_id,
            am.path AS image_url,
            rp.content AS update_text,
            COALESCE(r.last_activity, r.created_at) AS submitted_at,
            a.first_name,
            a.last_name
        FROM report_activity rp
        LEFT JOIN activity_media am ON am.activity_id = rp.activity_id
        LEFT JOIN reports r ON r.report_id = rp.report_id
        JOIN accounts a ON a.account_id = rp.account_id
        WHERE rp.activity_type = 'report_update'
        ORDER BY rp.activity_id DESC
    """)
    all_updates = cursor.fetchall()

    report_ids = [c.get('report_id') for c in all_concerns if c.get('report_id') is not None]
    feedbacks_by_report = {}
    feedback_counts_by_report = {}

    if report_ids:
        placeholders = ",".join(["%s"] * len(report_ids))
        feedback_query = f"""
            SELECT 
                f.activity_id AS feedback_id,
                f.report_id,
                f.account_id,
                f.content AS feedback,
                COALESCE(r.last_activity, r.created_at) AS uploaded_at,
                '' AS profile_photo,
                CONCAT(a.first_name, ' ', a.last_name) AS fullname
            FROM report_activity f
            LEFT JOIN reports r ON r.report_id = f.report_id
            LEFT JOIN accounts a ON a.account_id = f.account_id
            WHERE f.activity_type IN ('feedbacks', 'feedback') AND f.report_id IN ({placeholders})
            ORDER BY f.activity_id DESC
        """
        cursor.execute(feedback_query, tuple(report_ids))
        all_feedbacks = cursor.fetchall()
        now = datetime.now()
        for fb in all_feedbacks:
            if fb.get('uploaded_at'):
                diff = now - fb['uploaded_at']
                if diff.days > 7:
                    fb['time_ago'] = fb['uploaded_at'].strftime('%b %d, %Y')
                elif diff.days > 0:
                    fb['time_ago'] = f"{diff.days}d ago"
                else:
                    seconds = diff.seconds
                    if seconds >= 3600:
                        fb['time_ago'] = f"{seconds // 3600}h ago"
                    elif seconds >= 60:
                        fb['time_ago'] = f"{seconds // 60}m ago"
                    else:
                        fb['time_ago'] = "Just now"
            else:
                fb['time_ago'] = ""

            rid = fb.get('report_id')
            feedbacks_by_report.setdefault(rid, []).append(fb)

    for rid, fbs in feedbacks_by_report.items():
        feedback_counts_by_report[rid] = len(fbs)

    updates_by_report = {}
    for upd in all_updates:
        rid = upd.get('report_id')
        if rid is None:
            continue
        updates_by_report.setdefault(rid, []).append(upd)

    # ===== UPVOTES (from reports.upvote_count INT column) =====
    upvote_counts = {c['report_id']: int(c.get('upvote_count') or 0) for c in all_concerns if c.get('report_id') is not None}
    user_upvoted = set()

    account_id = session.get('user_id')
    if report_ids and account_id:
        placeholders = ",".join(["%s"] * len(report_ids))
        cursor.execute(
            f"""
            SELECT report_id FROM report_activity
            WHERE account_id = %s AND activity_type = 'upvote' AND report_id IN ({placeholders})
            """,
            (account_id,) + tuple(report_ids)
        )
        for row in cursor.fetchall():
            user_upvoted.add(row['report_id'])

    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo, 'Verified' AS account_status FROM accounts WHERE account_id = %s",
        (account_id,)
    )
    user_data = cursor.fetchone()
    con.close()

    return render_template(
        'file_concern.html',
        concerns=all_concerns,
        media_by_report=media_by_report,
        media_counts_by_report=media_counts_by_report,
        updates_by_report=updates_by_report,
        feedbacks_by_report=feedbacks_by_report,
        feedback_counts_by_report=feedback_counts_by_report,
        upvote_counts=upvote_counts,
        user_upvoted=user_upvoted,
        user=user_data
    )


# ===== API: Fetch report details by public_key (UUID) =====
@app.route('/api/report/<public_key>')
def api_report_by_key(public_key):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            r.report_id,
            r.public_key,
            r.title,
            r.description,
            'General' AS category,
            r.status,
            (SELECT rm.path FROM reports_media rm WHERE rm.report_id = r.report_id LIMIT 1) AS image_url,
            r.created_at,
            r.upvote_count,
            COALESCE(a.first_name, 'Resident') AS first_name,
            COALESCE(a.last_name, '') AS last_name,
            '' AS profile_photo,
            CONCAT(l.x, ', ', l.y) AS locname,
            l.x,
            l.y
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        LEFT JOIN location l ON r.location_id = l.location_id
        WHERE r.public_key = %s
    """, (public_key,))
    report = cursor.fetchone()

    if not report:
        con.close()
        return jsonify({'success': False, 'message': 'Report not found'}), 404

    for k, v in list(report.items()):
        if isinstance(v, (bytes, bytearray)):
            report[k] = v.decode('utf-8', errors='ignore') if v else ""
        elif isinstance(v, datetime):
            report[k] = v.strftime('%B %d, %Y - %I:%M %p')

    report['upvote_count'] = int(report.get('upvote_count') or 0)

    cursor.execute(
        "SELECT COUNT(*) as count FROM report_activity WHERE activity_type IN ('feedbacks', 'feedback') AND report_id = %s",
        (report['report_id'],)
    )
    report['comment_count'] = cursor.fetchone()['count']

    cursor.execute("""
        SELECT
            f.content AS feedback,
            COALESCE(r.last_activity, r.created_at) AS uploaded_at,
            CONCAT(a.first_name, ' ', a.last_name) AS fullname,
            '' AS profile_photo
        FROM report_activity f
        LEFT JOIN reports r ON r.report_id = f.report_id
        LEFT JOIN accounts a ON a.account_id = f.account_id
        WHERE f.activity_type IN ('feedbacks', 'feedback') AND f.report_id = %s
        ORDER BY f.activity_id DESC
        LIMIT 10
    """, (report['report_id'],))
    comments = cursor.fetchall()
    for c in comments:
        for k, v in list(c.items()):
            if isinstance(v, (bytes, bytearray)):
                c[k] = v.decode('utf-8', errors='ignore') if v else ""
            elif isinstance(v, datetime):
                c[k] = v.strftime('%b %d, %Y �?� %I:%M %p')

    report['comments'] = comments

    con.close()
    return jsonify({'success': True, 'report': report})


@app.route('/api/upvote', methods=['POST'])
def api_upvote():
    if 'user_id' not in session:
        return {'success': False, 'message': 'Not logged in'}, 401

    data = request.get_json()
    report_id = data.get('report_id')
    user_id = session.get('user_id')

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    # Check if already upvoted via report_activity
    cursor.execute("""
        SELECT activity_id FROM report_activity
        WHERE report_id = %s AND account_id = %s AND activity_type = 'upvote'
    """, (report_id, user_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("DELETE FROM report_activity WHERE activity_id = %s", (existing['activity_id'],))
        cursor.execute(
            "UPDATE reports SET upvote_count = GREATEST(0, COALESCE(upvote_count, 0) - 1) WHERE report_id = %s",
            (report_id,)
        )
        action = 'removed'
    else:
        cursor.execute(
            "INSERT INTO report_activity (account_id, report_id, activity_type, content) VALUES (%s, %s, 'upvote', 'upvote')",
            (user_id, report_id)
        )
        cursor.execute(
            "UPDATE reports SET upvote_count = COALESCE(upvote_count, 0) + 1 WHERE report_id = %s",
            (report_id,)
        )
        action = 'added'

    con.commit()

    cursor.execute("SELECT upvote_count FROM reports WHERE report_id = %s", (report_id,))
    row = cursor.fetchone()
    new_count = int(row['upvote_count']) if row and row['upvote_count'] is not None else 0
    con.close()

    return {'success': True, 'action': action, 'count': new_count}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        con = connect_db()
        cursor = con.cursor()

        try:
            data = request.form

            email = data.get('e', '').strip()
            phone = data.get('pn', '').strip()
            password = data.get('pass', '')
            conpass = data.get('conpass', '')

            if len(password) < 8:
                return render_template('register.html', error="Password must be at least 8 characters long")

            if password != conpass:
                return render_template('register.html', error="Passwords do not match")

            if phone:
                phone = phone.replace(' ', '')
                if phone.startswith('+63'):
                    phone = '0' + phone[3:]

                if not re.fullmatch(r'^09\d{9}$', phone):
                    return render_template('register.html', error="Invalid Philippine mobile number format")

            if not email and not phone:
                return render_template('register.html', error="Enter email or phone number")

            conditions = []
            check_values = []

            if email:
                conditions.append("email_address = %s")
                check_values.append(email)

            if phone:
                conditions.append("phone_number = %s")
                check_values.append(phone)

            # Updated for new ERD: registration.verified_at instead of otp_verified
            check_query = f"""
                SELECT registration_id, email_address, phone_number, verified_at
                FROM registration
                WHERE {' OR '.join(conditions)}
            """
            cursor.execute(check_query, tuple(check_values))
            existing_user = cursor.fetchone()

            if existing_user:
                existing_reg_id, existing_email, existing_phone, existing_verified_at = existing_user

                if existing_verified_at is None:
                    session['reg_id'] = existing_reg_id
                    session['otp_verified'] = False

                    otp_result = send_otp_sms(existing_phone)
                    if not otp_result.get('success'):
                        return render_template('register.html', error="OTP could not be sent. Please try again.")

                    return redirect(url_for('otpverify'))

                if email and existing_email == email:
                    return render_template('register.html', error="Email address is already in use")

                if phone and existing_phone == phone:
                    return render_template('register.html', error="Phone number is already in use")

                return render_template('register.html', error="Account already exists")

            hashed_pw = hash_password_bcrypt(password)

            # Updated for new ERD: registration.password_hash
            query = """
                INSERT INTO registration (email_address, phone_number, password_hash, verified_at)
                VALUES (%s, %s, %s, NULL)
            """
            values = (
                email if email else '',
                phone if phone else '',
                hashed_pw
            )

            cursor.execute(query, values)
            new_reg_id = cursor.lastrowid
            con.commit()

            session['reg_id'] = new_reg_id
            session['otp_verified'] = False

            otp_result = send_otp_sms(phone)
            if not otp_result.get('success'):
                print("OTP ERROR:", otp_result.get('error'))
                return render_template('register.html', error="Registration successful, but OTP could not be sent. Please try again.")

            return redirect(url_for('otpverify'))

        except Exception as e:
            con.rollback()
            print("REGISTRATION ERROR:", e)
            return render_template('register.html', error=f"Registration failed: {str(e)}")

        finally:
            cursor.close()
            con.close()

    return render_template('register.html')


@app.route('/otpverify', methods=['GET', 'POST'])
def otpverify():
    if 'reg_id' not in session:
        return redirect(url_for('register'))

    if 'otp' not in session:
        return redirect(url_for('register'))

    if request.method == 'POST':
        user_input_code = request.form.get('otp_code', '').strip()
        expected_code = session.get('otp')
        expires_at = session.get('otp_expires_at')

        if not user_input_code:
            return render_template('otp.html', error="Please enter the verification code.")

        if not expires_at:
            session.pop('otp', None)
            session.pop('otp_expires_at', None)
            return render_template('otp.html', error="OTP is no longer valid. Please request a new code.")

        if time.time() > expires_at:
            session.pop('otp', None)
            session.pop('otp_expires_at', None)
            return render_template('otp.html', error="OTP has expired. Please request a new code.")

        if user_input_code == expected_code:
            session.pop('otp', None)
            session.pop('otp_expires_at', None)
            session['otp_verified'] = True

            # Record verification timestamp in registration.verified_at
            try:
                con = connect_db()
                cursor = con.cursor()
                cursor.execute(
                    "UPDATE registration SET verified_at = %s WHERE registration_id = %s",
                    (datetime.now(), session['reg_id'])
                )
                con.commit()
                con.close()
            except Exception as e:
                print("Error updating verified_at:", e)

            return redirect(url_for('cd'))

        return render_template('otp.html', error="Invalid verification code. Please try again.")

    return render_template('otp.html')


@app.route('/complete_details', methods=['GET', 'POST'])
def cd():
    con = connect_db()
    cursor = con.cursor(buffered=True)
    reg_id = session.get('reg_id') or request.args.get('reg_id') or request.form.get('reg_id')

    if not reg_id:
        con.close()
        return redirect(url_for('login'))

    cred = "SELECT email_address, phone_number FROM registration WHERE registration_id = %s"
    cursor.execute(cred, (reg_id,))
    reg_user = cursor.fetchone()

    if request.method == 'GET':
        con.close()
        if reg_user:
            u = reg_user[0] or reg_user[1]
            return render_template('complete_details.html', u=u, reg_id=reg_id, email=reg_user[0] or '', phone=reg_user[1] or '')
        return redirect(url_for('login'))

    else:  # POST
        data = request.form

        cropped_image = data.get('cropped_image')
        if cropped_image and cropped_image.startswith('data:image'):
            header, encoded = cropped_image.split(",", 1)
            file_ext = header.split(";")[0].split("/")[1]
            filename = f"profile_{reg_id}_{int(datetime.now().timestamp())}.{file_ext}"
            os.makedirs('static/uploads', exist_ok=True)
            pp_path = f"static/uploads/{filename}"
            with open(pp_path, "wb") as fh:
                fh.write(base64.b64decode(encoded))

        # 1. Insert into contacts first (triggers passcontact -> usercreds -> insertuser -> credentials)
        cursor.execute(
            "INSERT INTO contacts (email, phone_number) VALUES (%s, %s)",
            (reg_user[0] if reg_user and reg_user[0] else None, reg_user[1] if reg_user and reg_user[1] else None)
        )
        new_contact_id = cursor.lastrowid

        # 2. Insert into address table (new ERD schema)
        cursor.execute("""
            INSERT INTO address (house_no, street, brgyorsubd, cityormunicipality, province, postalcode, country)
            VALUES (%s, %s, %s, %s, %s, %s, 'Philippines')
        """, (
            data.get('house_no'),
            data.get('street_name'),
            data.get('barangay_name'),
            data.get('city_name'),
            data.get('province_name'),
            data.get('postalcode')
        ))
        new_address_id = cursor.lastrowid

        # 3. Insert into accounts with contact_id, address_id, and middle_initial
        mname = (data.get('mname') or '').strip()
        middle_initial = mname[0].upper() if mname else ''

        cursor.execute("""
            INSERT INTO accounts (account_id, contact_id, address_id, first_name, last_name, middle_initial, dob)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            reg_id, new_contact_id, new_address_id,
            data.get('fname'), data.get('lname'), middle_initial, data.get('dob')
        ))
        newid = reg_id

        # 4. Copy password_hash from registration into password
        cursor.execute("""
            INSERT INTO password (password_hash)
            SELECT password_hash FROM registration WHERE registration_id = %s
        """, (reg_id,))
        new_pass_id = cursor.lastrowid

        # 5. Ensure credentials and user_role exist for all usercreds under this contact_id
        cursor.execute("SELECT user_id FROM usercreds WHERE contact_id = %s", (new_contact_id,))
        user_ids = [row[0] for row in cursor.fetchall()]

        for uid in user_ids:
            cursor.execute("SELECT cred_id, pass_id FROM credentials WHERE user_id = %s", (uid,))
            row = cursor.fetchone()
            if not row:
                cursor.execute(
                    "INSERT INTO credentials (user_id, pass_id, is_active, is_locked, is_banned) VALUES (%s, %s, 1, 'N', 0)",
                    (uid, new_pass_id)
                )
            elif row[1] is None:
                cursor.execute(
                    "UPDATE credentials SET pass_id = %s, is_active = 1, is_locked = 'N', is_banned = 0 WHERE cred_id = %s",
                    (new_pass_id, row[0])
                )

            cursor.execute("SELECT 1 FROM user_role WHERE user_id = %s", (uid,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)", (uid, 1))

        # 6. Delete temporary registration record
        cursor.execute("DELETE FROM registration WHERE registration_id = %s", (reg_id,))
        con.commit()
        con.close()

        session['pending_user_id'] = newid
        session.pop('reg_id', None)
        return redirect(url_for('id_verification'))


@app.route('/id_verification', methods=['GET', 'POST'])
def id_verification():
    if request.method == 'GET':
        user_id = session.get('pending_user_id')
        if not user_id:
            return redirect(url_for('login'))
        return render_template('id_verification.html', user_id=user_id)

    else:  # POST
        user_id = request.form.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        id_proof = request.files.get('id_proof')
        id_type = request.form.get('id_type', '').strip() or None
        id_proof_path = None
        if id_proof and id_proof.filename:
            os.makedirs('static/uploads/id_proofs', exist_ok=True)
            id_filename = f"id_{user_id}_{int(datetime.now().timestamp())}_{secure_filename(id_proof.filename)}"
            id_proof_path = f"static/uploads/id_proofs/{id_filename}"
            id_proof.save(id_proof_path)

        if not id_proof_path or not id_type:
            return render_template('id_verification.html', user_id=user_id, error="Please select an ID type and upload your valid ID")

        selfie = request.files.get('selfie')
        selfie_path = None
        if selfie and selfie.filename:
            os.makedirs('static/uploads/id_proofs', exist_ok=True)
            selfie_filename = f"selfie_{user_id}_{int(datetime.now().timestamp())}_{secure_filename(selfie.filename)}"
            selfie_path = f"static/uploads/id_proofs/{selfie_filename}"
            selfie.save(selfie_path)

        if not selfie_path:
            return render_template('id_verification.html', user_id=user_id, error="Please upload a selfie holding your ID")

        con = connect_db()
        cursor = con.cursor(buffered=True)
        cursor.execute("SELECT first_name FROM accounts WHERE account_id = %s", (user_id,))
        row = cursor.fetchone()
        user_name = row[0] if row else "Resident"
        con.close()

        session['user_id'] = user_id
        session['user_name'] = user_name
        session['user_role'] = 'resident'
        session.pop('pending_user_id', None)

        return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    cred_id = session.get('cred_id')
    emorph = session.get('emorph')
    if cred_id or emorph:
        try:
            con = connect_db()
            cursor = con.cursor()
            if cred_id:
                cursor.execute(
                    "UPDATE credentials SET is_active = 0, last_active_on = %s WHERE cred_id = %s",
                    (datetime.now(), cred_id)
                )
            cursor.execute(
                "INSERT INTO access_attempt (cred_id, credential_used, attempted_at, action) VALUES (%s, %s, %s, %s)",
                (cred_id, emorph, datetime.now(), 'Logout')
            )
            con.commit()
            cursor.close()
            con.close()
        except Exception as e:
            print("Error logging logout:", e)

    session.clear()
    return redirect(url_for('login'))


@app.route('/lgu_announcements', methods=['GET', 'POST'])
def lgu_announcements():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        account_id = session.get('user_id')

        if title and content:
            cursor.execute(
                "INSERT INTO announcements (account_id, category, ann_title, ann_desc, submitted_at) VALUES (%s, %s, %s, %s, %s)",
                (account_id, category, title, content, datetime.now())
            )
            con.commit()

        con.close()
        return redirect(url_for('lgu_announcements'))

    cursor.execute("SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s", (session['user_id'],))
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    cursor.execute("SELECT * FROM announcements ORDER BY submitted_at DESC")
    announcements_list = cursor.fetchall()
    for ann in announcements_list:
        if ann['submitted_at']:
            ann['formatted_date'] = ann['submitted_at'].strftime('%B %d, %Y')
        else:
            ann['formatted_date'] = ''

    con.close()

    return render_template('lgu_announcements.html', user=user_data, announcements=announcements_list)


@app.route('/delete_announcement/<int:ann_id>', methods=['POST'])
def delete_announcement(ann_id):
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM announcements WHERE ann_id = %s", (ann_id,))
    con.commit()
    con.close()
    return redirect(url_for('lgu_announcements'))


@app.route('/barangay_map')
def barangay_map():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s",
        (session['user_id'],)
    )
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    rep = """
        SELECT 
            r.report_id, 
            r.title, 
            'General' AS category, 
            r.description, 
            (SELECT rm.path FROM reports_media rm WHERE rm.report_id = r.report_id LIMIT 1) AS image_url, 
            r.status, 
            r.public_key,
            r.upvote_count,
            DATE_FORMAT(r.created_at, '%b %d, %Y %h:%i %p') AS created_at_str,
            CONCAT(l.x, ', ', l.y) AS locname, 
            l.x, 
            l.y, 
            COALESCE(CONCAT(a.first_name, ' ', a.last_name), 'Resident') AS reporter_name,
            '' AS reporter_photo
        FROM reports r
        JOIN location l ON r.location_id = l.location_id
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        WHERE l.x IS NOT NULL AND l.y IS NOT NULL
        ORDER BY r.created_at DESC
    """
    cursor.execute(rep)
    rloc = cursor.fetchall()

    # Fetch upvote history for the current user to highlight upvoted reports
    user_upvoted = set()
    account_id = session.get('user_id')
    if account_id:
        upvote_query = """
            SELECT report_id FROM report_activity
            WHERE account_id = %s AND activity_type = 'upvote'
        """
        cursor.execute(upvote_query, (account_id,))
        for row in cursor.fetchall():
            user_upvoted.add(row['report_id'])

    for r in rloc:
        r['is_upvoted'] = r['report_id'] in user_upvoted

    for r in rloc:
        for k, v in list(r.items()):
            if isinstance(v, (bytes, bytearray)):
                r[k] = v.decode('utf-8', errors='ignore') if v else ""
            elif v is None:
                r[k] = ""

    con.close()

    return render_template('barangay_map.html', user=user_data, rloc=rloc)


@app.route('/lgu_verifications')
def lgu_verifications():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s", (session['user_id'],))
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    # Updated for new ERD: accounts.contact_id = c.contact_id
    cursor.execute("""
        SELECT a.account_id, a.first_name, a.last_name, '' AS profile_photo,
               '' AS id_proof_path, c.email, c.phone_number
        FROM accounts a
        LEFT JOIN contacts c ON a.contact_id = c.contact_id
        WHERE 1=0
    """)
    pending_users = cursor.fetchall()
    con.close()

    return render_template('lgu_verifications.html', user=user_data, pending_users=pending_users)


@app.route('/verify_user', methods=['POST'])
def verify_user():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return redirect(url_for('login'))

    return redirect(url_for('lgu_verifications'))


@app.route('/lgu_analytics')
def lgu_analytics():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    account_id = session.get('user_id')

    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s",
        (account_id,)
    )
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    cursor.execute("SELECT COUNT(*) AS total FROM reports")
    total = cursor.fetchone()['total'] or 0

    cursor.execute("SELECT COUNT(*) AS cnt FROM reports WHERE LOWER(status) = 'pending'")
    pending = cursor.fetchone()['cnt'] or 0

    cursor.execute("SELECT COUNT(*) AS cnt FROM reports WHERE LOWER(status) IN ('in progress','inprogress','in_progress')")
    in_progress = cursor.fetchone()['cnt'] or 0

    cursor.execute("SELECT COUNT(*) AS cnt FROM reports WHERE LOWER(status) = 'resolved'")
    resolved = cursor.fetchone()['cnt'] or 0

    cursor.execute("SELECT COUNT(*) AS cnt FROM reports WHERE LOWER(status) IN ('denied', 'rejected', 'declined', 'cancelled', 'spam', 'invalid')")
    denied = cursor.fetchone()['cnt'] or 0

    cursor.execute("SELECT COUNT(*) AS cnt FROM reports WHERE DATE(created_at) = CURDATE()")
    today_count = cursor.fetchone()['cnt'] or 0

    cursor.execute("SELECT COUNT(*) AS cnt FROM reports WHERE YEARWEEK(created_at,1)=YEARWEEK(CURDATE(),1)")
    this_week = cursor.fetchone()['cnt'] or 0

    cursor.execute("""
        SELECT COUNT(*) AS cnt FROM reports
        WHERE YEAR(created_at) = YEAR(CURDATE()) AND MONTH(created_at) = MONTH(CURDATE())
    """)
    this_month = cursor.fetchone()['cnt'] or 0

    cursor.execute("""
        SELECT COUNT(*) AS cnt FROM reports
        WHERE YEAR(created_at) = YEAR(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
          AND MONTH(created_at) = MONTH(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
    """)
    last_month = cursor.fetchone()['cnt'] or 0

    # --- Engagement (Updated for new ERD: SUM(upvote_count) on reports & report_activity) ---
    cursor.execute("SELECT COALESCE(SUM(upvote_count), 0) AS cnt FROM reports")
    total_upvotes = int(cursor.fetchone()['cnt'] or 0)

    cursor.execute("SELECT COUNT(*) AS cnt FROM report_activity WHERE activity_type IN ('feedbacks', 'feedback')")
    total_comments = cursor.fetchone()['cnt'] or 0

    cursor.execute("SELECT COUNT(DISTINCT account_id) AS cnt FROM report_activity")
    total_residents = cursor.fetchone()['cnt'] or 0

    # --- Monthly trend (last 6 months) ---
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%b %Y') AS month_label,
               YEAR(created_at) AS yr, MONTH(created_at) AS mo,
               COUNT(*) AS cnt,
               SUM(CASE WHEN LOWER(status)='resolved' THEN 1 ELSE 0 END) AS resolved_cnt
        FROM reports
        WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY yr, mo, month_label ORDER BY yr ASC, mo ASC
    """)
    trend_rows = cursor.fetchall()
    monthly_labels = [r['month_label'] for r in trend_rows]
    monthly_counts = [r['cnt'] for r in trend_rows]
    monthly_resolved = [r['resolved_cnt'] for r in trend_rows]

    # --- Day-of-week distribution ---
    cursor.execute("""
        SELECT DAYOFWEEK(created_at) AS dow, COUNT(*) AS cnt
        FROM reports GROUP BY dow ORDER BY dow
    """)
    dow_map = {r['dow']: r['cnt'] for r in cursor.fetchall()}
    dow_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    dow_counts = [dow_map.get(i, 0) for i in range(1, 8)]

    # --- Week-of-month distribution ---
    cursor.execute("""
        SELECT CEIL(DAY(created_at) / 7) AS week_num, COUNT(*) AS cnt
        FROM reports 
        WHERE YEAR(created_at) = YEAR(CURDATE()) AND MONTH(created_at) = MONTH(CURDATE())
        GROUP BY week_num ORDER BY week_num
    """)
    wom_map = {r['week_num']: r['cnt'] for r in cursor.fetchall() if r['week_num']}
    wom_labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
    wom_counts = [wom_map.get(i, 0) for i in range(1, 6)]

    # --- Category breakdown ---
    category_data = [
        {'name': 'General', 'count': total, 'resolved': resolved, 'color': '#8b0000'}
    ] if total > 0 else []
    category_names = [c['name'] for c in category_data]
    category_counts = [c['count'] for c in category_data]

    # --- Top locations (from location x, y) ---
    cursor.execute("""
        SELECT CONCAT(l.x, ', ', l.y) AS locname, COUNT(*) AS cnt
        FROM reports r
        JOIN location l ON r.location_id = l.location_id
        GROUP BY l.location_id, l.x, l.y
        ORDER BY cnt DESC LIMIT 7
    """)
    top_locations = [
        {'locname': r['locname'], 'count': r['cnt']}
        for r in cursor.fetchall()
    ]

    # --- Top reporters ---
    cursor.execute("""
        SELECT a.first_name, a.last_name, COUNT(DISTINCT ra.report_id) AS cnt
        FROM report_activity ra
        JOIN accounts a ON ra.account_id = a.account_id
        GROUP BY ra.account_id, a.first_name, a.last_name
        ORDER BY cnt DESC LIMIT 5
    """)
    top_reporters = [
        {'name': f"{r['first_name']} {r['last_name']}",
         'count': r['cnt'],
         'initial': (r['first_name'] or 'U')[0].upper(),
         'photo': ''}
        for r in cursor.fetchall()
    ]

    # --- Oldest pending ---
    cursor.execute("""
        SELECT r.title, 'General' AS category, r.created_at,
               COALESCE(a.first_name, 'Resident') AS first_name,
               COALESCE(a.last_name, '') AS last_name,
               DATEDIFF(CURDATE(), DATE(r.created_at)) AS days_old
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        WHERE LOWER(r.status) = 'pending'
        ORDER BY r.created_at ASC LIMIT 5
    """)
    oldest_pending = cursor.fetchall()

    # --- Recent 10 reports ---
    cursor.execute("""
        SELECT r.report_id, r.title, 'General' AS category, r.status, r.created_at,
               COALESCE(a.first_name, 'Resident') AS first_name,
               COALESCE(a.last_name, '') AS last_name,
               CONCAT(l.x, ', ', l.y) AS locname
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        LEFT JOIN location l ON r.location_id = l.location_id
        ORDER BY r.created_at DESC LIMIT 10
    """)
    recent_reports = cursor.fetchall()

    # --- Sample report ---
    cursor.execute("""
        SELECT r.report_id, r.title, 'General' AS category, r.description, r.status, r.created_at,
               COALESCE(a.first_name, 'Resident') AS first_name,
               COALESCE(a.last_name, '') AS last_name,
               CONCAT(l.x, ', ', l.y) AS locname
        FROM reports r
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        LEFT JOIN location l ON r.location_id = l.location_id
        ORDER BY RAND() LIMIT 1
    """)
    sample_report = cursor.fetchone()

    con.close()

    stats = {
        'total': total, 'pending': pending,
        'in_progress': in_progress, 'resolved': resolved,
        'denied': denied,
        'today': today_count, 'this_week': this_week,
        'this_month': this_month, 'last_month': last_month,
        'total_upvotes': total_upvotes,
        'total_comments': total_comments,
        'total_residents': total_residents,
    }

    monthly_summary, sample_summary, status_summary, location_summary, category_summary = generate_monthly_analytics_summary(
        monthly_labels, monthly_counts, monthly_resolved, sample_report, stats, top_locations, category_data
    )

    return render_template(
        'lgu_analytics.html',
        user=user_data,
        stats=stats,
        monthly_labels=monthly_labels,
        monthly_counts=monthly_counts,
        monthly_resolved=monthly_resolved,
        dow_labels=dow_labels,
        dow_counts=dow_counts,
        wom_labels=wom_labels,
        wom_counts=wom_counts,
        category_data=category_data,
        category_names=category_names,
        category_counts=category_counts,
        top_locations=top_locations,
        top_reporters=top_reporters,
        oldest_pending=oldest_pending,
        recent_reports=recent_reports,
        sample_report=sample_report,
        monthly_summary=monthly_summary,
        sample_summary=sample_summary,
        status_summary=status_summary,
        location_summary=location_summary,
        category_summary=category_summary
    )


@app.route('/lgu_map')
def lgu_map():
    if 'user_id' not in session or session.get('user_role') != 'lgu':
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)

    cursor.execute(
        "SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s",
        (session['user_id'],)
    )
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    rep = """
        SELECT 
            r.report_id, 
            r.title, 
            'General' AS category, 
            r.description, 
            (SELECT rm.path FROM reports_media rm WHERE rm.report_id = r.report_id LIMIT 1) AS image_url, 
            r.status, 
            r.public_key,
            r.upvote_count,
            DATE_FORMAT(r.created_at, '%b %d, %Y %h:%i %p') AS created_at_str,
            CONCAT(l.x, ', ', l.y) AS locname, 
            l.x, 
            l.y, 
            COALESCE(CONCAT(a.first_name, ' ', a.last_name), 'Resident') AS reporter_name,
            '' AS reporter_photo
        FROM reports r
        JOIN location l ON r.location_id = l.location_id
        LEFT JOIN (
            SELECT report_id, MIN(account_id) AS account_id
            FROM report_activity
            GROUP BY report_id
        ) ra ON ra.report_id = r.report_id
        LEFT JOIN accounts a ON ra.account_id = a.account_id
        WHERE l.x IS NOT NULL AND l.y IS NOT NULL
        ORDER BY r.created_at DESC
    """
    cursor.execute(rep)
    rloc = cursor.fetchall()

    for r in rloc:
        for k, v in list(r.items()):
            if isinstance(v, (bytes, bytearray)):
                r[k] = v.decode('utf-8', errors='ignore') if v else ""
            elif v is None:
                r[k] = ""

    con.close()

    return render_template('lgu_map.html', user=user_data, rloc=rloc)


@app.route('/announcements')
def announcements():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = connect_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT first_name, last_name, '' AS profile_photo FROM accounts WHERE account_id = %s", (session['user_id'],))
    user_rows = cursor.fetchall()
    user_data = user_rows[0] if user_rows else None

    cursor.execute("""
        SELECT a.*, acc.first_name, acc.last_name 
        FROM announcements a
        LEFT JOIN accounts acc ON a.account_id = acc.account_id
        ORDER BY a.submitted_at DESC
    """)
    db_anns = cursor.fetchall()

    anns_list = []
    emoji_map = {
        'General': '📢',
        'Health': '🏥',
        'Infrastructure': '🛣️',
        'Events': '🎉',
        'Safety': '🚨'
    }

    for row in db_anns:
        cat = row['category'] or 'General'
        emoji = emoji_map.get(cat, '📢')
        author = f"{row['first_name']} {row['last_name']}" if row['first_name'] else "Barangay Picaleon"
        date_str = row['submitted_at'].strftime('%B %d, %Y') if row['submitted_at'] else ''

        anns_list.append({
            'cat': cat.lower(),
            'emoji': emoji,
            'tag': f"{emoji} {cat}",
            'title': row['ann_title'],
            'excerpt': (row['ann_desc'][:100] + '...') if row['ann_desc'] and len(row['ann_desc']) > 100 else (row['ann_desc'] or ''),
            'date': date_str,
            'author': author,
            'views': '-',
            'content': f"<p>{row['ann_desc']}</p>"
        })

    con.close()

    anns_json = json.dumps(anns_list)

    return render_template('announcements.html', user=user_data, announcements_json=anns_json)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
