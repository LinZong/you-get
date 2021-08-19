import json

# save info from common.print_info()
last_info = None


class VideoExtractorCodec(object):
    def encode(self, video_extractor):
        pass

    def decode(self, video_extractor, encoded_data):
        pass


class VideoExtractorJsonCodec(VideoExtractorCodec):
    def __init__(self, pretty=True):
        super(VideoExtractorJsonCodec, self).__init__()
        self.pretty = pretty

    def encode(self, video_extractor):
        ve = video_extractor
        out = {}
        out['url'] = ve.url
        out['title'] = ve.title
        out['vid'] = ve.vid
        out['m3u8_url'] = ve.m3u8_url
        out['site'] = ve.name
        out['streams'] = ve.streams
        out['dash_streams'] = {}
        out['streams_sorted'] = ve.streams_sorted
        out['caption_tracks'] = ve.caption_tracks
        out['danmaku'] = ve.danmaku
        out['lyrics'] = ve.lyrics
        try:
            if ve.dash_streams:
                out['dash_streams'].update(ve.dash_streams)
        except AttributeError:
            pass
        try:
            if ve.audiolang:
                out['audiolang'] = ve.audiolang
        except AttributeError:
            pass
        extra = {}
        if getattr(ve, 'referer', None) is not None:
            extra["referer"] = ve.referer
        if getattr(ve, 'ua', None) is not None:
            extra["ua"] = ve.ua
        if extra:
            out["extra"] = extra
        if self.pretty:
            return json.dumps(out, indent=4, ensure_ascii=False)
        else:
            return json.dumps(out)

    def decode(self, video_extractor, encoded_data):
        video_extractor.url = encoded_data['url']
        video_extractor.title = encoded_data['title']
        video_extractor.name = encoded_data['site']
        video_extractor.streams = encoded_data['streams']
        video_extractor.streams_sorted = encoded_data.get('streams_sorted', [])
        video_extractor.caption_tracks = encoded_data.get('caption_tracks', {})
        video_extractor.dash_streams = encoded_data.get('dash_streams', {})
        video_extractor.audiolang = encoded_data.get('audiolang', None)
        video_extractor.danmaku = encoded_data.get('danmaku')
        video_extractor.lyrics = encoded_data.get('lyrics')
        extra = encoded_data.get('extra')
        if extra is not None:
            video_extractor.referer = extra.get('referer')
            video_extractor.ua = extra.get('ua')


def output(video_extractor, pretty_print=True):
    ve = video_extractor
    out = {}
    out['url'] = ve.url
    out['title'] = ve.title
    out['site'] = ve.name
    out['streams'] = ve.streams
    try:
        if ve.dash_streams:
            out['streams'].update(ve.dash_streams)
    except AttributeError:
        pass
    try:
        if ve.audiolang:
            out['audiolang'] = ve.audiolang
    except AttributeError:
        pass
    extra = {}
    if getattr(ve, 'referer', None) is not None:
        extra["referer"] = ve.referer
    if getattr(ve, 'ua', None) is not None:
        extra["ua"] = ve.ua
    if extra:
        out["extra"] = extra
    if pretty_print:
        print(json.dumps(out, indent=4, ensure_ascii=False))
    else:
        print(json.dumps(out))

# a fake VideoExtractor object to save info
class VideoExtractor(object):
    pass

def print_info(site_info=None, title=None, type=None, size=None):
    global last_info
    # create a VideoExtractor and save info for download_urls()
    ve = VideoExtractor()
    last_info = ve
    ve.name = site_info
    ve.title = title
    ve.url = None

def download_urls(urls=None, title=None, ext=None, total_size=None, refer=None):
    ve = last_info
    if not ve:
        ve = VideoExtractor()
        ve.name = ''
        ve.url = urls
        ve.title=title
    # save download info in streams
    stream = {}
    stream['container'] = ext
    stream['size'] = total_size
    stream['src'] = urls
    if refer:
        stream['refer'] = refer
    stream['video_profile'] = '__default__'
    ve.streams = {}
    ve.streams['__default__'] = stream
    output(ve)
