from database.DB_connect import DBConnect
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllNodes(year1, year2):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = ("SELECT distinct d.* "
                 "FROM drivers d, results r, races ra"
                 "WHERE d.driverId = r.driverId and r.raceId = ra.raceID"
                 "and ra.year between %s and %s"
                 "and r.position is not null"
                 "order by d.driverId")
        cursor.execute(query, (year1, year2,))
        for row in cursor:
            results.append(Driver(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(year1, year2, idMapDriver):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId aas d1, r2.driverId as d2, count(*) as peso
                    from results r1, results r2, races r
                    where r.raceId = r1.raceId and r.raceId = r2.raceId
                    and r1.constructorId = r2.constructorId
                    and r1.driverId > r2.driverId
                    and r1.position is not null
                    and r2.position is not null
                    and r.year between %s and %s
                    group by r1.driverId, r2.driverId
                    order by peso desc"""
        cursor.execute(query, (year1, year2,))
        for row in cursor:
            results.append(Arco(idMapDriver[row['d1']], idMapDriver[row['d2']], row['peso']))
        cursor.close()
        conn.close()
        return results

