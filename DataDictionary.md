// 找诊所  联系选中诊所【预约】
// 提醒狗吃药
// forum vets need verification
// gallery optional
// 推送tips 【clinics 发布广告】
// 病例史
// 打分 (相亲)?

- Pet owners
- licensed vet clinics, vet clinics, 
- daily pet care feature
- medication reminder
- hygiene reminder
- exercise reminder
- forum
- users and vets
- Administrator
- system administrators



### Data Dictionary on Problem Domain:

- **iPet Platform**: The web, android and iOS version of **iPet Platform** developed by **<Team liangLiang>**

- **User**: Including registered **Pet Owners**, registered **Vets**, registered **Clinics** and **Visitors**.

    - **Pet Owners**: Pet owners who has registered on the Platform with critical information (Username, Phone No., Pet Breed and Pet Age)

    - **Licensed Vet, Vet**: Vets that registered with critical information (Username, Phone No., Lisence No.) and verified by the administrator.
    
    - **Licensed Vet Clinic, Vet Clinic, Clinic**: Pet health services providers who are listed in the government open-source database and have registered on the **iPet Platform** with critical information (Username, Phone No., address and softcopy of the clinic license).
 
    - **Visitor**: People who visit the platform and are not registered, or are registered without critical information

- **Reminder**: Information generated by the **iPet Platform** according to the medical history retrieved from **Clinics** through **API System**, or according to the information uploaded by the **Pet Owner**
 
- **API system**: Ports, charged or free, designed for **Licensed Vet Clinics** to access the **iPet Platform** system.
