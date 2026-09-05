import plotly.graph_objects as go
import plotly.express as px

def apply_chart_theme(fig: go.Figure) -> go.Figure:
    """
    Apply dark modern theme layout parameters to Plotly chart figures.
    """
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="Inter, sans-serif", size=12, color="#E2E8F0"),
        margin=dict(l=20, r=20, t=50, b=20),
        title_font=dict(size=16, color="#F8FAFC", family="Inter, sans-serif"),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.08)",
            zerolinecolor="rgba(255, 255, 255, 0.15)",
            showgrid=True
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.08)",
            zerolinecolor="rgba(255, 255, 255, 0.15)",
            showgrid=True
        )
    )
    return fig
