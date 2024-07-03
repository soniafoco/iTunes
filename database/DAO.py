from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAlbums():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.*, sum(t.Milliseconds) as Duration
                    from album a, track t
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId 
                    order by a.Title asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAlbumPlaylist(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t1.AlbumId as a1, t2.AlbumId as a2
                    from playlisttrack p1, playlisttrack p2, track t1, track t2
                    where p1.TrackId = t1.TrackId and p2.TrackId = t2.TrackId 
                    and t1.AlbumId > t2.AlbumId and p1.PlaylistId = p2.PlaylistId  """

        cursor.execute(query)

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append( (idMap[row["a1"]], idMap[row["a2"]]) )

        cursor.close()
        conn.close()
        return result

