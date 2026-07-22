import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from supabase import create_client, Client
from PIL import Image

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="☕ Brew & Bean Coffee",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SUPABASE CONNECTION
# ==========================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "logged_in": False,
    "username": "",
    "role": "",
    "cart": [],
    "customer": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
    if "page" not in st.session_state:
     st.session_state.page = "🏠 Home"

st.markdown("## ☕ Brew & Bean Coffee")

c1,c2,c3,c4,c5,c6,c7,c8 = st.columns(8)

with c1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "🏠 Home"

with c2:
    if st.button("📖 Menu", use_container_width=True):
        st.session_state.page = "📖 Menu"

with c3:
    if st.button("🛒 Cart", use_container_width=True):
        st.session_state.page = "🛒 Cart"

with c4:
    if st.button("💳 Payment", use_container_width=True):
        st.session_state.page = "💳 Payment"

with c5:
    if st.button("📝 Signup", use_container_width=True):
        st.session_state.page = "📝 Signup"

with c6:
    if st.button("👤 My Account", use_container_width=True):
        st.session_state.page = "👤 My Account"

with c7:
    if st.button("📞 Contact", use_container_width=True):
        st.session_state.page = "📞 Contact"

with c8:
    if st.button("👨‍💼 Admin", use_container_width=True):
        st.session_state.page = "👨‍💼 Admin"

page = st.session_state.page    

# ==========================================
# CREATE DEFAULT ADMIN
# ==========================================

try:

    admin = (
        supabase.table("users")
        .select("*")
        .eq("username", "admin")
        .execute()
    )

    if len(admin.data) == 0:

        supabase.table("users").insert({

            "username": "admin",
            "password": "1234",
            "email": "admin@gmail.com",
            "role": "admin"

        }).execute()

except:
    pass

# ==========================================
# GOOGLE FONT
# ==========================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)
# ==========================================
# PREMIUM CSS
# ==========================================
import streamlit as st

st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

/* Background */
.stApp{
    background:linear-gradient(135deg,#090909,#141414,#1f1f1f);
    color:white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#111111,#1c1c1c);
    border-right:2px solid #D4AF37;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Main Container */
.block-container{
    background:rgba(20,20,20,.55);
    border:1px solid rgba(212,175,55,.4);
    border-radius:20px;
    padding:2rem;
    box-shadow:0 0 25px rgba(212,175,55,.18);
}

/* Headings */
h1,h2,h3,h4,h5,h6{
    color:#FFD700;
    font-weight:700;
}

/* Buttons */
.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#D4AF37,#FFD700);
    color:black;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:16px;
    font-weight:bold;
    transition:.3s;
}

.stButton>button:hover{
    transform:translateY(-3px);
    box-shadow:0 0 20px gold;
}

/* Text Input */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea{
    background:#222;
    color:white;
    border:2px solid #D4AF37;
    border-radius:10px;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"]{
    background:#222;
    border-radius:10px;
    border:2px solid #D4AF37;
}

/* DataFrame */
[data-testid="stDataFrame"]{
    border:2px solid #D4AF37;
    border-radius:15px;
    overflow:hidden;
}

/* Metric */
[data-testid="metric-container"]{
    background:#181818;
    border:1px solid #D4AF37;
    border-radius:15px;
    padding:15px;
    box-shadow:0 0 15px rgba(212,175,55,.2);
}

/* Cards */
.card{
    background:#181818;
    border:1px solid #D4AF37;
    border-radius:20px;
    padding:20px;
    box-shadow:0 0 20px rgba(212,175,55,.2);
}

/* Success */
.stSuccess{
    background:#0d2818;
    border-left:6px solid #00ff88;
}

/* Warning */
.stWarning{
    background:#3a2800;
    border-left:6px solid orange;
}

/* Error */
.stError{
    background:#330000;
    border-left:6px solid red;
}

/* Info */
.stInfo{
    background:#001d33;
    border-left:6px solid #00bfff;
}

/* Tables */
table{
    border-collapse:collapse;
}

thead{
    background:#D4AF37;
    color:black;
}

tbody tr:nth-child(even){
    background:#1f1f1f;
}

/* Images */
img{
    border-radius:15px;
    border:2px solid #D4AF37;
}

/* Scrollbar */
::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-thumb{
    background:#D4AF37;
    border-radius:10px;
}

/* Responsive */
@media(max-width:768px){

.block-container{
    padding:1rem;
}

h1{
    font-size:28px;
}

.stButton>button{
    font-size:15px;
}

section[data-testid="stSidebar"]{
    width:100% !important;
}

}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
# ==========================================







# ==========================================
# LOGIN SYSTEM
# ==========================================

if st.session_state.logged_in:


    st.sidebar.success(
        f"👋 Welcome {st.session_state.username}"
    )


    if st.sidebar.button("🚪 Logout"):


        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()



else:


    st.sidebar.subheader(
        "🔐 Login"
    )


    login_user = st.sidebar.text_input(
        "Username"
    )


    login_pass = st.sidebar.text_input(
        "Password",
        type="password"
    )


    if st.sidebar.button("Login"):


        result = (

            supabase.table("users")
            .select("*")
            .eq("username",login_user)
            .eq("password",login_pass)
            .execute()

        )


        if result.data:


            user = result.data[0]


            st.session_state.logged_in = True

            st.session_state.username = user["username"]

            st.session_state.role = user["role"]


            st.success(
                "✅ Login Successful"
            )


            st.rerun()



        else:

            st.error(
                "❌ Invalid Username or Password"
            )



# ==========================================
# ADMIN LIVE ORDERS SIDEBAR
# ==========================================

if (

    st.session_state.logged_in

    and

    st.session_state.role=="admin"

):


    st.sidebar.divider()


    st.sidebar.subheader(
        "📦 Live Orders"
    )


    try:


        orders = (

            supabase.table("orders")
            .select("*")
            .order("id",desc=True)
            .execute()

        )


        st.sidebar.metric(

            "Total Orders",

            len(orders.data)

        )


        for order in orders.data[:5]:


            st.sidebar.info(

                f"""
☕ {order['item']}

👤 {order['customer']}

Qty : {order['quantity']}

₹ {order['total']}
"""

            )


    except:


        st.sidebar.warning(
            "No Orders Found"
        )
# ==========================================
# LOAD MENU FROM SUPABASE
# ==========================================

def load_menu():

    response = (
        supabase
        .table("menu")
        .select("*")
        .order("id")
        .execute()
    )

    return pd.DataFrame(response.data)



# ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.markdown(
        "<div class='title'>☕ Brew & Bean Coffee</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Fresh Coffee • Fresh Moments • Every Cup Tells A Story</div>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown("""
        <div style='
            background:rgba(255,255,255,.08);
            padding:25px;
            border-radius:20px;
            border:1px solid gold;
            box-shadow:0 10px 25px black;
        '>

        <h2>Welcome To Brew & Bean ☕</h2>

        <p style='font-size:18px;'>

        ✔ Premium Coffee<br>
        ✔ Organic Beans<br>
        ✔ Fresh Desserts<br>
        ✔ Fast Service<br>
        ✔ Free Wi-Fi

        </p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "☕ Order Now",
            key="home_order_btn"
        ):
            st.success("Open Menu Page From Sidebar")

    with col2:

        st.image(
            "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
            use_container_width=True
        )

    st.divider()

    st.subheader("🔥 Best Sellers")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div style='
            background:rgba(255,255,255,.08);
            padding:20px;
            border-radius:18px;
            text-align:center;
            border:1px solid gold;
        '>

        <h2>☕ Espresso</h2>

        <h3 style='color:gold;'>₹150</h3>

        ⭐⭐⭐⭐⭐

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div style='
            background:rgba(255,255,255,.08);
            padding:20px;
            border-radius:18px;
            text-align:center;
            border:1px solid gold;
        '>

        <h2>☕ Cappuccino</h2>

        <h3 style='color:gold;'>₹180</h3>

        ⭐⭐⭐⭐⭐

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div style='
            background:rgba(255,255,255,.08);
            padding:20px;
            border-radius:18px;
            text-align:center;
            border:1px solid gold;
        '>

        <h2>☕ Latte</h2>

        <h3 style='color:gold;'>₹220</h3>

        ⭐⭐⭐⭐⭐

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    a, b, c, d = st.columns(4)

    a.metric("☕ Coffee", "30+")
    b.metric("🍰 Desserts", "20+")
    c.metric("😊 Customers", "12K+")
    d.metric("⭐ Rating", "4.9 / 5")

    st.divider()

    st.info("⏰ Open Daily : 9:00 AM - 10:00 PM")

    st.success("📍 Pune, Maharashtra")



# ==========================================
# MENU PAGE
# ==========================================

elif page == "📖 Menu":


    st.markdown(
        "<h1 class='title'>☕ Coffee Menu</h1>",
        unsafe_allow_html=True
    )


    menu_df = load_menu()


    if menu_df.empty:

        st.warning(
            "No Menu Available"
        )


    else:


        cols = st.columns(3)


        for index,coffee in menu_df.iterrows():


            with cols[index%3]:


                st.markdown(
                    "<div class='card'>",
                    unsafe_allow_html=True
                )


                if coffee["image"]:


                    st.image(
                        coffee["image"],
                        use_container_width=True
                    )


                else:

                    st.info(
                        "No Image"
                    )


                st.subheader(
                    coffee["name"]
                )


                st.write(
                    "₹",
                    coffee["price"]
                )


                qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=1,
                    key=f"qty{index}"
                )


                if st.button(
                    "Add Cart",
                    key=f"cart{index}"
                ):


                    item={

                    "name":coffee["name"],
                    "price":coffee["price"],
                    "quantity":qty,
                    "total":coffee["price"]*qty

                    }


                    st.session_state.cart.append(item)


                    st.success(
                        "Added To Cart"
                    )


                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                ) 
# ==========================================
# CART PAGE
# ==========================================

elif page == "🛒 Cart":


    st.markdown(
        "<h1 class='title'>🛒 Your Cart</h1>",
        unsafe_allow_html=True
    )


    if len(st.session_state.cart)==0:


        st.warning(
            "Cart is Empty"
        )


    else:


        cart_df = pd.DataFrame(
            st.session_state.cart
        )


        st.dataframe(
            cart_df,
            use_container_width=True
        )


        total = cart_df["total"].sum()


        st.metric(
            "Total Amount",
            f"₹ {total}"
        )


        customer = st.text_input(
            "Customer Name",
            value=st.session_state.customer
        )


        if st.button(
            "Place Order"
        ):


            if customer=="":

                st.error(
                    "Enter Customer Name"
                )


            else:


                for item in st.session_state.cart:


                    supabase.table("orders").insert({

                        "customer":customer,

                        "item":item["name"],

                        "quantity":item["quantity"],

                        "total":item["total"],

                        "date":str(datetime.now())

                    }).execute()



                st.success(
                    "✅ Order Placed Successfully"
                )


                st.session_state.cart=[]


                st.rerun() 
# ==========================================
# PAYMENT PAGE
# ==========================================

elif page == "💳 Payment":


    st.markdown(
        "<h1 class='title'>💳 Payment</h1>",
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="card">

        Scan QR Code and Pay ☕

        </div>
        """,
        unsafe_allow_html=True
    )


    try:

        st.image(
            "assets/payment_qr.png",
            width=300
        )


        st.success(
            "UPI Payment Available"
        )


    except:

        st.warning(
            "Payment QR Not Found"
        )


    st.info(
        """
        UPI ID:
        
        brewbean@upi
        
        After payment, confirm your order.
        """
    )
# ==========================================
# SIGNUP PAGE
# ==========================================

elif page == "📝 Signup":


    st.markdown(
        "<h1 class='title'>📝 Create Account</h1>",
        unsafe_allow_html=True
    )


    new_user = st.text_input(
        "Username"
    )


    new_email = st.text_input(
        "Email"
    )


    new_password = st.text_input(
        "Password",
        type="password"
    )


    if st.button(
        "Create Account"
    ):


        if new_user=="" or new_password=="":


            st.error(
                "Please fill all details"
            )


        else:


            check = (

                supabase
                .table("users")
                .select("*")
                .eq("username",new_user)
                .execute()

            )


            if check.data:


                st.warning(
                    "Username already exists"
                )


            else:


                supabase.table("users").insert({

                    "username":new_user,

                    "password":new_password,

                    "email":new_email,

                    "role":"customer"

                }).execute()


                st.success(
                    "✅ Account Created Successfully"
                )
# ==========================================
# MY ACCOUNT PAGE
# ==========================================

elif page == "👤 My Account":


    st.markdown(
        "<h1 class='title'>👤 My Account</h1>",
        unsafe_allow_html=True
    )


    if st.session_state.logged_in:


        username = st.session_state.username


        # USER DETAILS

        user = (

            supabase
            .table("users")
            .select("*")
            .eq("username",username)
            .execute()

        )


        if user.data:


            data = user.data[0]


            st.markdown(
                """
                <div class="card">

                </div>
                """,
                unsafe_allow_html=True
            )


            st.subheader(
                "Account Details"
            )


            st.write(
                "👤 Username :",
                data["username"]
            )


            st.write(
                "📧 Email :",
                data["email"]
            )


            st.write(
                "🔑 Role :",
                data["role"]
            )



        # ORDER HISTORY

        st.divider()


        st.subheader(
            "📦 My Orders"
        )


        orders = (

            supabase
            .table("orders")
            .select("*")
            .eq("customer",username)
            .execute()

        )


        if orders.data:


            order_df = pd.DataFrame(
                orders.data
            )


            st.dataframe(
                order_df,
                use_container_width=True
            )


        else:

            st.info(
                "No Orders Found"
            )



    else:


        st.warning(
            "Please Login First"
        
        )
elif page == "📞 Contact":

    st.markdown(
        "<div class='title'>📞 Contact Us</div>",
        unsafe_allow_html=True
    )

    st.info("""
📍 **Address**
Narhe, Maharashtra

📞 **Phone**
+91 1234567890

📧 **Email**
brewbean@gmail.com

🕘 **Opening Hours**
9:00 AM – 10:00 PM
""")

    st.map(pd.DataFrame({
        "lat": [18.191863],
        "lon": [73.859373]
    }))
    st.link_button(
    "📍 Open in Google Maps",
    "https://maps.google.com/?q=18.191863,73.859373"
)
        
# ==========================================
# ADMIN DASHBOARD
# ==========================================

elif page == "👨‍💼 Admin":


    st.markdown(
        "<h1 class='title'>👨‍💼 Admin Dashboard</h1>",
        unsafe_allow_html=True
    )


    if (
        st.session_state.logged_in
        and
        st.session_state.role=="admin"
    ):


        # ===============================
        # ORDERS
        # ===============================


        st.subheader(
            "📦 All Orders"
        )


        orders = (

            supabase
            .table("orders")
            .select("*")
            .order("id",desc=True)
            .execute()

        )


        if orders.data:


            order_df = pd.DataFrame(
                orders.data
            )


            st.dataframe(
                order_df,
                use_container_width=True
            )


            total_sales = order_df["total"].sum()


            col1,col2 = st.columns(2)


            with col1:

                st.metric(
                    "Total Orders",
                    len(order_df)
                )


            with col2:

                st.metric(
                    "Total Sales",
                    f"₹ {total_sales}"
                )


        else:


            st.info(
                "No Orders Available"
            )



        st.divider()



        # ===============================
        # USERS
        # ===============================


        st.subheader(
            "👥 Customers"
        )


        users = (

            supabase
            .table("users")
            .select("*")
            .execute()

        )


        if users.data:


            user_df = pd.DataFrame(
                users.data
            )


            st.dataframe(
                user_df,
                use_container_width=True
            )



        st.divider()



        # ===============================
        # MENU VIEW
        # ===============================


        st.subheader(
            "☕ Menu Items"
        )


        menu = (

            supabase
            .table("menu")
            .select("*")
            .execute()

        )


        if menu.data:


            menu_df = pd.DataFrame(
                menu.data
            )


            st.dataframe(
                menu_df,
                use_container_width=True
            )

        # ==========================================
# ADMIN MENU MANAGEMENT
# ==========================================

        st.divider()

        st.subheader(
                  "➕ Add New Menu Item"
            )


        menu_name = st.text_input(
                "Coffee Name"
        )


        menu_price = st.number_input(
            "Price",
            min_value=1
        )


        menu_image = st.file_uploader(
            "Upload Coffee Image",
            type=["png","jpg","jpeg"]
        )


        if st.button("Add Menu Item"):


            if menu_name=="" or menu_image is None:

                st.error(
                    "Enter name and upload image"
                )


            else:


             file_name = (
                str(uuid.uuid4())
                    + ".jpg"
                )


            image_bytes = menu_image.read()


                # Upload Image To Supabase Storage

            supabase.storage\
                .from_("coffee-images")\
                .upload(
                    file_name,
                    image_bytes,
                    {
                        "content-type":"image/jpeg"
                    }
                )
     

                # Get Public URL

            image_url = (

                    supabase.storage
                    .from_("coffee-images")
                    .get_public_url(file_name)

                )


                # Save Menu Data

            supabase.table("menu").insert({

                    "name":menu_name,

                    "price":menu_price,

                    "image":image_url

                }).execute()



            st.success(
                    "☕ Menu Added With Image"
                )


            st.rerun()
          
        
    else:


         st.error(
            "❌ Admin Login Required"
         )   
       
