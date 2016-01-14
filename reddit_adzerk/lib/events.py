from pylons import app_globals as g

from r2.lib.eventcollector import (
    EventQueue,
    Event,
    squelch_exceptions,
)
from r2.lib.utils import sampled
from r2.models import (
    FakeSubreddit,
)


class AdEvent(Event):
    @classmethod
    def get_context_data(cls, request, context):
        data = super(AdEvent, cls).get_context_data(request, context)
        dnt_header = request.headers.get("DNT", None)

        if dnt_header is not None:
            data["dnt"] = dnt_header == "1"

        return data


class AdEventQueue(EventQueue):
    @squelch_exceptions
    @sampled("events_collector_ad_serving_sample_rate")
    def ad_request(
            self,
            keywords,
            platform,
            placement_name,
            placement_types,
            is_refresh,
            subreddit=None,
            request=None,
            context=None,
        ):
        """Create an `ad_request` for event-collector.

        keywords: Array of keywords used to select the ad.
        platform: The platform the ad was requested for.
        placement_name: The identifier of the placement.
        placement_types: Array of placements types.
        is_refresh: Whether or not the request is for the initial ad or a
            refresh after refocusing the page.
        subreddit: The Subreddit of the ad was  displayed on.
        request, context: Should be pylons.request & pylons.c respectively;

        """
        event = AdEvent(
            topic="ad_serving_events",
            event_type="ss.ad_request",
            request=request,
            context=context,
        )

        event.add("keywords", keywords)
        event.add("platform", platform)
        event.add("placement_name", placement_name)
        event.add("placement_types", placement_types)
        event.add("is_refresh", is_refresh)

        if not isinstance(subreddit, FakeSubreddit):
            event.add_subreddit_fields(subreddit)

        self.save_event(event)

    @squelch_exceptions
    @sampled("events_collector_ad_serving_sample_rate")
    def ad_response(
            self,
            keywords,
            platform,
            placement_name,
            placement_types,
            ad_id,
            link_id=None,
            campaign_id=None,
            subreddit=None,
            request=None,
            context=None,
        ):
        """Create an `ad_response` for event-collector.

        keywords: Array of keywords used to select the ad.
        platform: The platform the ad was requested for.
        placement_name: The identifier of the placement.
        placement_types: Array of placements types.
        ad_id: Unique id of the ad response.
        link_id: The id of the promoted link.
        subreddit: The Subreddit of the ad was  displayed on.
        request, context: Should be pylons.request & pylons.c respectively;

        """
        event = AdEvent(
            topic="ad_serving_events",
            event_type="ss.ad_response",
            request=request,
            context=context,
        )

        event.add("keywords", keywords)
        event.add("platform", platform)
        event.add("placement_name", placement_name)
        event.add("placement_types", placement_types)
        event.add("ad_id", ad_id)
        event.add("link_id", link_id)
        event.add("campaign_id", campaign_id)

        if not isinstance(subreddit, FakeSubreddit):
            event.add_subreddit_fields(subreddit)

        self.save_event(event)