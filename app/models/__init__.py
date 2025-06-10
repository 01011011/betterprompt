"""
Database models for BetterPrompt application.

This module contains all SQLAlchemy models for the application including
Users, Prompts, Usage logs, and Subscriptions.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, Text, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY, ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
import enum

from app.database import db


class UserPlanType(enum.Enum):
    """User subscription plan types."""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(enum.Enum):
    """Subscription status types."""
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"
    INCOMPLETE = "incomplete"


class PromptStatus(enum.Enum):
    """Prompt processing status types."""
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(UserMixin, db.Model):
    """
    User model for authentication and user management.
    
    Supports multiple OAuth providers and stores user preferences and subscription info.
    """
    __tablename__ = 'users'
    
    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=False), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    
    # OAuth provider information
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # 'microsoft', 'google', 'github'
    provider_id: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # User profile
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Account status and plan
    plan_type: Mapped[UserPlanType] = mapped_column(ENUM(UserPlanType), default=UserPlanType.FREE, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    prompts: Mapped[List["Prompt"]] = relationship("Prompt", back_populates="user", cascade="all, delete-orphan")
    usage_logs: Mapped[List["UsageLog"]] = relationship("UsageLog", back_populates="user", cascade="all, delete-orphan")
    subscriptions: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_users_provider_composite', 'provider', 'provider_id'),
        Index('idx_users_email_active', 'email', 'is_active'),
    )
    
    def __init__(self, email: str, provider: str, provider_id: str, **kwargs):
        """Initialize user with required fields."""
        self.email = email
        self.provider = provider
        self.provider_id = provider_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f'<User {self.email} ({self.provider})>'
    
    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.now(timezone.utc)
        db.session.commit()
    
    def get_current_subscription(self) -> Optional["Subscription"]:
        """Get the user's current active subscription."""
        return Subscription.query.filter_by(
            user_id=self.id, 
            status=SubscriptionStatus.ACTIVE
        ).first()
    
    def get_monthly_usage_count(self) -> int:
        """Get the user's prompt count for the current month."""
        now = datetime.now(timezone.utc)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        return Prompt.query.filter(
            Prompt.user_id == self.id,
            Prompt.created_at >= start_of_month,
            Prompt.status == PromptStatus.COMPLETED
        ).count()
    
    def can_create_prompt(self) -> bool:
        """Check if user can create a new prompt based on their plan limits."""
        usage_count = self.get_monthly_usage_count()
        
        # Plan limits
        limits = {
            UserPlanType.FREE: 5,
            UserPlanType.BASIC: 100,
            UserPlanType.PRO: 1000,
            UserPlanType.ENTERPRISE: float('inf')
        }
        
        return usage_count < limits.get(self.plan_type, 0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'uuid': self.uuid,
            'email': self.email,
            'display_name': self.display_name,
            'avatar_url': self.avatar_url,
            'plan_type': self.plan_type.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'monthly_usage': self.get_monthly_usage_count()
        }


class Prompt(db.Model):
    """
    Prompt model for storing user prompts and their optimizations.
    
    Stores both original and optimized prompts with metadata and processing info.
    """
    __tablename__ = 'prompts'
    
    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Prompt content
    original_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    optimized_prompt: Mapped[Optional[str]] = mapped_column(Text)
    
    # Processing metadata
    model_used: Mapped[str] = mapped_column(String(100), nullable=False, default='o1-mini')
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[PromptStatus] = mapped_column(ENUM(PromptStatus), default=PromptStatus.PROCESSING, nullable=False)
    
    # User organization
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="prompts")
    usage_logs: Mapped[List["UsageLog"]] = relationship("UsageLog", back_populates="prompt")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_prompts_user_created', 'user_id', 'created_at'),
        Index('idx_prompts_status', 'status'),
        Index('idx_prompts_favorites', 'user_id', 'is_favorite'),
        Index('idx_prompts_tags_gin', 'tags', postgresql_using='gin'),
    )
    
    def __init__(self, user_id: int, original_prompt: str, **kwargs):
        """Initialize prompt with required fields."""
        self.user_id = user_id
        self.original_prompt = original_prompt
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f'<Prompt {self.id} by User {self.user_id}>'
    
    def mark_completed(self, optimized_prompt: str, tokens_used: int = None, processing_time_ms: int = None) -> None:
        """Mark prompt as completed with results."""
        self.optimized_prompt = optimized_prompt
        self.status = PromptStatus.COMPLETED
        if tokens_used is not None:
            self.tokens_used = tokens_used
        if processing_time_ms is not None:
            self.processing_time_ms = processing_time_ms
        self.updated_at = datetime.now(timezone.utc)
    
    def mark_failed(self) -> None:
        """Mark prompt as failed."""
        self.status = PromptStatus.FAILED
        self.updated_at = datetime.now(timezone.utc)
    
    def toggle_favorite(self) -> None:
        """Toggle the favorite status."""
        self.is_favorite = not self.is_favorite
        self.updated_at = datetime.now(timezone.utc)
    
    def add_tags(self, tags: List[str]) -> None:
        """Add tags to the prompt."""
        if self.tags is None:
            self.tags = []
        self.tags = list(set(self.tags + tags))  # Remove duplicates
        self.updated_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert prompt to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'original_prompt': self.original_prompt,
            'optimized_prompt': self.optimized_prompt,
            'model_used': self.model_used,
            'tokens_used': self.tokens_used,
            'processing_time_ms': self.processing_time_ms,
            'status': self.status.value,
            'is_favorite': self.is_favorite,
            'tags': self.tags or [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class UsageLog(db.Model):
    """
    Usage tracking model for monitoring user activity and billing.
    
    Tracks all user actions for analytics, billing, and rate limiting.
    """
    __tablename__ = 'usage_logs'
    
    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    prompt_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('prompts.id', ondelete='SET NULL'))
    
    # Action tracking
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # 'optimize_prompt', 'view_history', etc.
    tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cost_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Cost in cents
    
    # Flexible metadata storage
    metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="usage_logs")
    prompt: Mapped[Optional["Prompt"]] = relationship("Prompt", back_populates="usage_logs")
    
    # Indexes for analytics
    __table_args__ = (
        Index('idx_usage_logs_user_date', 'user_id', 'created_at'),
        Index('idx_usage_logs_action_date', 'action', 'created_at'),
    )
    
    def __init__(self, user_id: int, action: str, **kwargs):
        """Initialize usage log with required fields."""
        self.user_id = user_id
        self.action = action
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f'<UsageLog {self.action} by User {self.user_id}>'
    
    @classmethod
    def log_action(cls, user_id: int, action: str, prompt_id: int = None, 
                   tokens_used: int = 0, cost_cents: int = 0, metadata: Dict[str, Any] = None) -> "UsageLog":
        """Create and save a usage log entry."""
        log_entry = cls(
            user_id=user_id,
            action=action,
            prompt_id=prompt_id,
            tokens_used=tokens_used,
            cost_cents=cost_cents,
            metadata=metadata or {}
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert usage log to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'action': self.action,
            'prompt_id': self.prompt_id,
            'tokens_used': self.tokens_used,
            'cost_cents': self.cost_cents,
            'metadata': self.metadata or {},
            'created_at': self.created_at.isoformat()
        }


class Subscription(db.Model):
    """
    Subscription model for managing user billing and plan access.
    
    Integrates with Stripe for payment processing and tracks subscription status.
    """
    __tablename__ = 'subscriptions'
    
    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Stripe integration
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    
    # Subscription details
    plan_type: Mapped[UserPlanType] = mapped_column(ENUM(UserPlanType), nullable=False)
    status: Mapped[SubscriptionStatus] = mapped_column(ENUM(SubscriptionStatus), nullable=False, index=True)
    
    # Billing periods
    current_period_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Usage tracking
    monthly_quota: Mapped[int] = mapped_column(Integer, nullable=False)
    quota_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")
    
    # Indexes
    __table_args__ = (
        Index('idx_subscriptions_user_status', 'user_id', 'status'),
        Index('idx_subscriptions_period_end', 'current_period_end'),
    )
    
    def __init__(self, user_id: int, plan_type: UserPlanType, status: SubscriptionStatus, **kwargs):
        """Initialize subscription with required fields."""
        self.user_id = user_id
        self.plan_type = plan_type
        self.status = status
        self.monthly_quota = self._get_plan_quota(plan_type)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f'<Subscription {self.plan_type.value} for User {self.user_id}>'
    
    @staticmethod
    def _get_plan_quota(plan_type: UserPlanType) -> int:
        """Get the monthly quota for a plan type."""
        quotas = {
            UserPlanType.FREE: 5,
            UserPlanType.BASIC: 100,
            UserPlanType.PRO: 1000,
            UserPlanType.ENTERPRISE: 10000  # High but not unlimited for safety
        }
        return quotas.get(plan_type, 5)
    
    def is_active(self) -> bool:
        """Check if subscription is currently active."""
        return self.status == SubscriptionStatus.ACTIVE
    
    def has_quota_remaining(self) -> bool:
        """Check if user has quota remaining."""
        return self.quota_used < self.monthly_quota
    
    def use_quota(self, amount: int = 1) -> bool:
        """Use quota if available."""
        if self.quota_used + amount <= self.monthly_quota:
            self.quota_used += amount
            self.updated_at = datetime.now(timezone.utc)
            return True
        return False
    
    def reset_quota(self) -> None:
        """Reset monthly quota (called at billing period start)."""
        self.quota_used = 0
        self.updated_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert subscription to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'plan_type': self.plan_type.value,
            'status': self.status.value,
            'monthly_quota': self.monthly_quota,
            'quota_used': self.quota_used,
            'quota_remaining': self.monthly_quota - self.quota_used,
            'current_period_start': self.current_period_start.isoformat() if self.current_period_start else None,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
