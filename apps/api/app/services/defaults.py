"""Starter data created for every new household."""

from app.models import AccountKind, CategoryKind

DEFAULT_ACCOUNT = {
    "name": "Carteira",
    "kind": AccountKind.CASH,
    "color": "#56ab91",
    "icon": "wallet",
}

# (name, lucide icon, color)
EXPENSE_CATEGORIES: list[tuple[str, str, str]] = [
    ("Moradia", "house", "#076ebd"),
    ("Mercado", "shopping-cart", "#12ae6c"),
    ("Restaurantes", "utensils", "#fea519"),
    ("Transporte", "car", "#42b5e7"),
    ("Saúde", "heart-pulse", "#f83215"),
    ("Educação", "graduation-cap", "#2b478b"),
    ("Lazer", "party-popper", "#fa4deb"),
    ("Contas e serviços", "receipt", "#4d72cc"),
    ("Assinaturas", "tv", "#8b5cf6"),
    ("Compras", "shopping-bag", "#d76060"),
    ("Vestuário", "shirt", "#ec4899"),
    ("Pets", "paw-print", "#b45309"),
    ("Presentes", "gift", "#e11d48"),
    ("Impostos e taxas", "landmark", "#64748b"),
    ("Viagens", "plane", "#0ea5e9"),
    ("Cuidados pessoais", "sparkles", "#f472b6"),
    ("Outros gastos", "ellipsis", "#98a6af"),
]

INCOME_CATEGORIES: list[tuple[str, str, str]] = [
    ("Salário", "briefcase", "#35aa3a"),
    ("Freelance", "laptop", "#56ab91"),
    ("Investimentos", "trending-up", "#076ebd"),
    ("Vendas", "store", "#fea519"),
    ("Bônus", "award", "#8b5cf6"),
    ("Aluguel recebido", "key-round", "#42b5e7"),
    ("Reembolsos", "rotate-ccw", "#64748b"),
    ("Outras receitas", "circle-plus", "#98a6af"),
]


def default_categories() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for kind, items in (
        (CategoryKind.EXPENSE, EXPENSE_CATEGORIES),
        (CategoryKind.INCOME, INCOME_CATEGORIES),
    ):
        for position, (name, icon, color) in enumerate(items):
            rows.append(
                {"name": name, "kind": kind, "icon": icon, "color": color, "position": position}
            )
    return rows
