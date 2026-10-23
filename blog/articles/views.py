from django.http import Http404
from django.shortcuts import render

from .models import Article, Enterprise, ExchangeRate, IndicatorValue


def archive(request):
    """Show all analyst articles; each title links to its detail page."""
    posts = Article.objects.select_related("author").order_by("-created_date", "-id")
    return render(request, "archive.html", {"posts": posts})


def get_article(request, article_id):
    """Show a single article selected by its numeric database ID."""
    try:
        post = Article.objects.select_related("author").get(id=article_id)
    except Article.DoesNotExist as exc:
        raise Http404("Статья не найдена") from exc
    return render(request, "article.html", {"post": post})


def financial_dashboard(request):
    """Overview of financial indicators and exchange rates for variant 24."""
    enterprises = Enterprise.objects.all()
    values = IndicatorValue.objects.select_related(
        "enterprise", "report_period", "indicator"
    ).order_by("-report_period__start_date", "enterprise__name", "indicator__name")
    rates = ExchangeRate.objects.all().order_by("-effective_date")[:30]
    return render(
        request,
        "financial_dashboard.html",
        {"enterprises": enterprises, "indicator_values": values, "exchange_rates": rates},
    )
