from normality import stringify
from flask_babel import gettext
from urlnormalizer import normalize_url
from followthemoney import model
from followthemoney.types import registry
from jsonschema import FormatChecker

from aleph import settings
from aleph.model import Collection


checker = FormatChecker()


@checker.checks("locale", raises=ValueError)
def check_locale(value):
    value = stringify(value)
    if value not in settings.UI_LANGUAGES:
        raise ValueError(gettext('Invalid user locale.'))
    return True


@checker.checks("country", raises=ValueError)
def check_country_code(value):
    value = registry.country.clean(value)
    if not registry.country.validate(value):
        msg = gettext('Invalid country code: %s')
        raise ValueError(msg % value)
    return True


@checker.checks("category", raises=ValueError)
def check_category(value):
    if value not in Collection.CATEGORIES.keys():
        raise ValueError(gettext('Invalid category.'))
    return True


@checker.checks("url", raises=ValueError)
def check_url(value):
    value = stringify(value)
    if value is not None and normalize_url(value) is None:
        raise ValueError(gettext('Invalid URL.'))
    return True


@checker.checks("language", raises=ValueError)
def check_language(value):
    value = registry.language.clean(value)
    if not registry.language.validate(value):
        raise ValueError(gettext('Invalid language code.'))
    return True


@checker.checks("schema", raises=ValueError)
def check_schema(value):
    schema = model.get(value)
    if schema is None:
        msg = gettext('Invalid schema name: %s')
        raise ValueError(msg % value)
    return True


@checker.checks("partial-date", raises=ValueError)
def check_partial_date(value):
    if not registry.date.validate(value):
        raise ValueError(gettext('Invalid date: %s') % value)
    return True
