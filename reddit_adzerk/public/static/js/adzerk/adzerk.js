r.adzerk = {
    origin: location.protocol == 'https:'
            ? 'https://az.turbobytes.net'
            : 'http://static.adzerk.net',

    spots: [],

    createAds: function(frameNames) {
        frameNames = _.object(_.compact(frameNames.split(',')), [])

        var omitted = []
        _.each(this.spots, function(spot) {
            if (_.has(frameNames, spot.frameName)) {
                spot.show()
            } else {
                omitted.push(spot)
            }
        }, this)

        _.invoke(omitted, 'hide')
    }
}

r.adzerk.IFrameSpot = function(options) {
    this.options = options
    this.frameName = options.frameName
}
r.adzerk.IFrameSpot.prototype = {
    show: function() {
        var adSrc = r.adzerk.origin + '/r2/ads-load.html' + '#frame_' + this.frameName
        $('<iframe>')
            .attr({
                'id': this.options.frameId,
                'src': adSrc,
                'frameBorder': 0,
                'scrolling': 'no'
            })
            .appendTo($(this.options.container).empty())
    },

    hide: function() {
        $(this.options.container).empty()
    }
}

r.adzerk.spots.push(new r.adzerk.IFrameSpot({
    frameName: 'sponsorship',
    frameId: 'ad_sponsorship',
    container: '.side .sponsorshipbox'
}))

r.adzerk.spots.push(new r.adzerk.IFrameSpot({
    frameName: 'side_box',
    frameId: 'ad-frame',
    container: '.side .ad-side-box'
}))

$(window).on('message', function(ev) {
    ev = ev.originalEvent
    if (ev.origin != r.adzerk.origin) {
      return
    }
    msg = ev.data.split(':')
    if (msg[0] == 'ados.createAds') {
      r.adzerk.createAds(msg[1])
    }
})
