import streamlit as st
import datetime
import os
import smtplib
from email.mime.text import MIMEText

# ----- EMAIL NOTIFICATION SETTINGS -----
# The App Password is read from Streamlit's "Secrets" (see secrets.toml),
# so it never has to be typed directly into this file or pushed to GitHub.
SENDER_EMAIL = "shreyphysicaltherapist@gmail.com"
SENDER_APP_PASSWORD = st.secrets.get("GMAIL_APP_PASSWORD", "")
RECEIVER_EMAIL = "shreyphysicaltherapist@gmail.com"


def send_booking_email(name, phone, age, appt_date, notes, source):
    subject = f"New Appointment Booking - {name}"
    body = f"""New patient booking received via PhysioConnect:

Registration Type: {source}
Patient Name: {name}
Contact Number: {phone}
Age: {age}
Preferred Date: {appt_date}
Notes: {notes}
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    if not SENDER_APP_PASSWORD:
        return False, "GMAIL_APP_PASSWORD not set in Secrets yet."

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)

# Page Configuration for Mobile Responsiveness
st.set_page_config(page_title="Dr. Shrey Pandey", page_icon="🩺", layout="centered")

# Main Header
st.title("🩺 Dr. Shrey Pandey")
st.subheader("Physiotherapy & Patient Management")
st.markdown("---")

# Navigation Menu for Mobile Layout
menu = st.radio("Go to:", ["📋 Smart Planner", "📅 Bookings & Referrals", "👨‍⚕️ About Dr. Shrey"], horizontal=True)

# 1. SMART PLANNER
if menu == "📋 Smart Planner":
    st.header("🧠 Smart Treatment Planner")

    problem = st.selectbox(
        "Select Injury / Condition:",
        [
            "Acute Lower Back Spasm (Short-Term)",
            "Minor Ankle Sprain / Neck Strain (Short-Term)",
            "Frozen Shoulder / Post-Fracture Stiffness (Mid-Term)",
            "Ligament Sprains Grade I/II (Mid-Term)",
            "Stroke Rehabilitation (Long-Term)",
            "ACL Reconstruction Recovery (Long-Term)",
            "Chronic Sciatica / Osteoarthritis (Long-Term)"
        ]
    )

    st.markdown("### 📊 Recovery Roadmap")
    if "Short-Term" in problem:
        st.success("🟩 **Category: Short-Term (Acute/Minor)**")
        st.write("⏱️ **Cure Time:** 2 to 4 Weeks")
        st.write("📅 **Frequency:** 2-3 Sessions per week")
        st.write("🎯 **Focus:** Pain Relief & Immediate Mobility")
    elif "Mid-Term" in problem:
        st.warning("🟨 **Category: Mid-Term (Moderate)**")
        st.write("⏱️ **Cure Time:** 1 to 3 Months")
        st.write("📅 **Frequency:** 2 Sessions per week")
        st.write("🎯 **Focus:** Strength Rebuilding & Muscle Recovery")
    elif "Long-Term" in problem:
        st.error("🟥 **Category: Long-Term (Chronic/Severe)**")
        st.write("⏱️ **Cure Time:** 3 to 6+ Months")
        st.write("📅 **Frequency:** 1-2 Sessions per week")
        st.write("🎯 **Focus:** Lifestyle Adaptation & Full Independence")

# 2. BOOKINGS & REFERRALS
elif menu == "📅 Bookings & Referrals":

    st.header("🔗 Patient Intake & Referral Gateway")

    source = st.selectbox("Registration Type:", ["Direct Patient Booking", "Doctor / Clinic Referral"])

    with st.form("booking_form", clear_on_submit=True):
        p_name = st.text_input("Patient Full Name*")
        p_phone = st.text_input("Contact Number*")
        p_age = st.number_input("Patient Age", min_value=1, max_value=120, value=30)
        appt_date = st.date_input("Preferred Date", min_value=datetime.date.today())

        if source == "Doctor / Clinic Referral":
            doc_name = st.text_input("Referring Doctor Name / Hospital")
            doc_notes = st.text_area("Clinical Notes / Instructions")
        else:
            doc_notes = st.text_area("Describe your pain/symptoms")

        submit = st.form_submit_button("Confirm Booking")
        if submit:
            if p_name and p_phone:
                sent, error = send_booking_email(
                    name=p_name,
                    phone=p_phone,
                    age=p_age,
                    appt_date=appt_date,
                    notes=doc_notes,
                    source=source,
                )
                st.balloons()
                st.success(f"🎉 Success! Appointment booked for {p_name}. Dr. Shrey's team will call you soon.")
                if not sent:
                    st.warning(f"(Note: booking saved, but the email notification could not be sent: {error})")
            else:
                st.error("Please fill Name and Contact Number.")

# 3. ABOUT DR. SHREY
elif menu == "👨‍⚕️ About Dr. Shrey":

    st.header("👨‍⚕️ Clinician Profile")

    # Photo
    photo_path = os.path.join(os.path.dirname(__file__), "doctor_photo.jpg")
    if os.path.exists(photo_path):
        st.image(photo_path, width=220, caption="Dr. Shrey Pandey")

    st.markdown("""
    **Dr. Shrey Pandey** *BPT, MPT | Consultant Physiotherapist*

    **Core Specializations:**
    * 🏃‍♂️ Sports Injury Rehabilitation
    * 🧠 Neurological Rehabilitation (Stroke, Paralysis)
    * 🦴 Orthopedic & Post-Surgery Care
    * 👵 Geriatric Mobility Management

    **Certifications:** 📜 Certified OHS Professional | Certified Manual Therapist
    """)

    st.markdown("---")
    st.markdown("### 📞 Contact Information")
    st.write("📱 **Phone:** +91 63065 89612")
    st.write("📧 **Email:** shreyphysicaltherapist@gmail.com")
    st.write("📍 **Address:** 26/A, Manohar Vihar, Yashoda Nagar, Kanpur Nagar, Uttar Pradesh")
