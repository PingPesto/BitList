from .song import Song
import datetime
from pyramid_mongoengine import MongoEngine

db = MongoEngine()


class Playlist(db.Document):

    songs = db.ListField(db.ReferenceField(Song), default=[])
    name = db.StringField(required=True)

    @classmethod
    def get(cls, name='default'):
        pl = cls.objects(name=name).first()
        return pl

    def add(self, request, song_id):
        song = Song.get_by_id(song_id)
        self.songs.append(song)
        self.save()
        # use either request object, or player client
        # passed in from job context
        try:
            request.mpd.add(song.url)
        except AttributeError:
            request.add(song.url)
        return self.songs

    def compare(self, request):
        ''' Pass in a request object or a player.client instance.
            This method will return the diff between the active
            mpd playlist, and the document playlist '''
        try:
            mpd_playlist = request.mpd.playlist()
        except AttributeError:
            mpd_playlist = request.playlist()
        for i in xrange(len(mpd_playlist)):
            mpd_playlist[i] = mpd_playlist[i].replace('file: ', '')
        this_playlist = []
        for x in self.songs:
            this_playlist.append(x.url)
        return self._diff(this_playlist, mpd_playlist)



    def _diff(self, a, b):
        ''' Helper method to compute the diff between 2 arrays '''
        b = set(b)
        return [aa for aa in a if aa not in b]

    def sync_with_mpd(self, request):
        ''' use this method to sync with the MPD daemon. This keeps the
            document song list in sync w/ MPD Daemons currently playing list.
            Does not add songs added by other means... which can be problematic
            but ideally you're managing your MPD daemon with bitlist right?
        '''
        urls = self.compare(request)
        for u in urls:
            s = Song.get_by_url(u)
            Playlist.objects(name=self.name).update_one(pull__songs=s.id)
        self.reload()
        return self.songs
