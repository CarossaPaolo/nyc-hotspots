from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllProviders():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT DISTINCT n.Provider 
        FROM nyc_wifi_hotspot_locations n
        ORDER BY n.Provider 
        """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row[0])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getLocalitaByProvider(provider):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT DISTINCT n.Location 
        FROM nyc_wifi_hotspot_locations n
        WHERE n.Provider = %s
        """
        cursor.execute(query, (provider,))

        res = []
        for row in cursor:
            res.append(row[0])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getCorrelazioni(provider):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT n.Location, AVG(n.Latitude) as lat, AVG(n.Longitude) as lng
        FROM nyc_wifi_hotspot_locations n
        WHERE n.Provider = %s
        GROUP BY n.Location
        """
        cursor.execute(query, (provider,))

        res = {}
        for row in cursor:
            res[row[0]] = (row[1], row[2])

        cursor.close()
        conn.close()
        return res
