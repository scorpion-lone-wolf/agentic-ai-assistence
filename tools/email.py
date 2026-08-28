from security import RiskLevel
from tool import Tool
from pydantic import ConfigDict
from pydantic import Field
from pydantic import BaseModel


class SendEmailArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recipient: str = Field(
        max_length=100,
        min_length=1,
        description="Email address of the recipient",
    )
    subject: str = Field(
        max_length=100,
        min_length=1,
        description="Subject of the email",
    )
    body: str = Field(
        max_length=1000,
        min_length=1,
        description="Body of the email",
    )


def send_email(
    recipient: str,
    subject: str,
    body: str,
) -> str:
    """
    Simulated email sender.

    Later this implementation can be replaced
    by Gmail, SMTP, SES, etc.
    """

    print("\n========== SIMULATED EMAIL SENT ==========")

    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print()
    print(body)

    return f"Email successfully sent to {recipient}."


email_tool = Tool(
    name="send_email",
    description=(
        "Send an email to a recipient. "
        "Use this only when the user explicitly requests "
        "that an email be sent."
    ),
    function=send_email,
    args_model=SendEmailArgs,
    risk_level=RiskLevel.WRITE,
)
