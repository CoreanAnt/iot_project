import pymysql as ps

db = ps.connect(
        host="localhost",
        user="root",
        passwd="1234",
        db="test",
        charset="utf8")

cursor = db.cursor()

def insertSensor1(temperature) :
    sql = f"insert into sensordb(sensing) values({temperature})"
    cursor.execute(sql)
    db.commit()

def insertSensor2(humidity) :
    sql = f"insert into sensordb(sensing) values({humidity})"
    cursor.execute(sql)
    db.commit()

def insertSensor3(adc1) :
    sql = f"insert into sensordb(sensing) values({adc1})"
    cursor.execute(sql)
    db.commit()

def insertSensor4(adc2) :
    sql = f"insert into sensordb(sensing) values({adc2})"
    cursor.execute(sql)
    db.commit()