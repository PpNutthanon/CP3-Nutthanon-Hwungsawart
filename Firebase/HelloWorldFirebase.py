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

# Todo As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('Users')
ref2 = db.reference('TextDemo')
ref3 = db.reference("Users/Pp/age")
ref4 = db.reference("Users/Pp")
print(ref.get(),ref2.get())
print(ref3.get())
print(ref4.get())


#Todo เพิ่มข้อมูลลงไปใน ref(เรากำหนดให้ไปใส่ใน Users) => ดูจากบรรทัดที่ 16

posts_ref = ref.child('posts')

new_post_ref = posts_ref.push()
new_post_ref.set({
    'author': 'gracehop',
    'title': 'Announcing COBOL, a New Programming Language'
})

# We can also chain the two calls together
posts_ref.push().set({
    'author': 'alanisawesome',
    'title': 'The Turing Machine'
})

# Todo Update ข้อมูลที่อยู่ในระบบ(แก้ไขข้อมูลเดิม)
hopper_ref = users_ref.child('gracehop')
hopper_ref.update({
    'nickname': 'Amazing Grace'
})