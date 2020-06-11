from hypothesis import Verbosity
from hypothesis import settings as hypo_settings

from iheroes_api.config.environment import get_settings

settings = get_settings()


# Configure Hypothesis profiles
hypo_settings.register_profile(
    "development", max_examples=10, verbosity=Verbosity.verbose
)
hypo_settings.register_profile("ci", max_examples=1000)

hypo_settings.load_profile(settings.HYPOTHESIS_PROFILE)
