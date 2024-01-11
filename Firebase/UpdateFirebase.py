# Database => แหล่งเก็บข้อมูลจำนวนมาก(เป็นระเบียบ), สามารถเพิ่มและลบข้อมูลได้, ดึงข้อมูลได้เท่าที่เราขอมา(ประหยัดพื้นที่)
# Todo In this course we using "Firebase" database => ใช้หลักการคล้ายๆ Json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Todo Fetch the service account key JSON file contents
cred = credentials.Certificate("helloworld-f87e0-firebase-adminsdk-lxpsl-7ce9f6243e.json")

# Todo Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://helloworld-f87e0-default-rtdb.firebaseio.com/"
})

#! Path ที่อยู่ของข้อมูลต้อง check ดีๆนะ
ref = db.reference("")
hopper_ref = ref.child('gracehop')
hopper_ref.update({
    'nickname': 'Amazing Grace1234'
})

