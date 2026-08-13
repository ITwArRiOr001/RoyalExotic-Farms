"""
app/models.py — persistence for form submissions and analytics events.

Submission stores every inquiry/partnership/contact message (full persistence at
launch, per Final Requirements). AnalyticsEvent stores lightweight, dashboard-
ready events (page views, form starts/success, clicks) with no third-party
tracker required.
"""
from datetime import datetime
from .extensions import db


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(32), nullable=False, index=True)  # inquiry|partner|contact
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    locale = db.Column(db.String(8))

    # Shared contact fields
    name = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    email = db.Column(db.String(320), nullable=False, index=True)
    phone = db.Column(db.String(64))
    country = db.Column(db.String(120))
    message = db.Column(db.Text)
    consent = db.Column(db.Boolean, default=False, nullable=False)

    # Contact-specific
    enquiry_type = db.Column(db.String(64))

    # Inquiry-specific
    product = db.Column(db.String(64))
    quantity = db.Column(db.String(120))
    consultation = db.Column(db.Boolean, default=False)

    # Partnership-specific
    product_lines = db.Column(db.String(300))
    volume = db.Column(db.String(120))
    frequency = db.Column(db.String(64))
    target_market = db.Column(db.String(200))

    # Request metadata (spam triage / audit)
    ip = db.Column(db.String(64))
    user_agent = db.Column(db.String(400))

    def __repr__(self):
        return f"<Submission {self.kind} #{self.id} {self.email}>"


class AnalyticsEvent(db.Model):
    __tablename__ = "analytics_events"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    type = db.Column(db.String(48), nullable=False, index=True)  # pageview|form_start|form_success|click
    path = db.Column(db.String(500))
    referrer = db.Column(db.String(500))
    locale = db.Column(db.String(8))
    session_id = db.Column(db.String(64), index=True)
    meta = db.Column(db.JSON)

    def __repr__(self):
        return f"<AnalyticsEvent {self.type} {self.path}>"
