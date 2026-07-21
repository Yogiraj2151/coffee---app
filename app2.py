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

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html,body,[class*="css"]{
    font-family:'Poppins',sans-serif;
}

.stApp{

    background:
    linear-gradient(
    rgba(15,15,15,0.75),
    rgba(15,15,15,0.75)
    ),
    url("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085");

    background-size:cover;
    background-attachment:fixed;
}


header, footer{
    visibility:hidden;
}


section[data-testid="stSidebar"]{

    background:
    rgba(20,20,20,0.95);

    backdrop-filter:blur(15px);

}


.stButton > button{

    width:100%;
    border-radius:15px;
    background:#D4AF37;
    color:black;
    font-weight:700;
    border:none;

}


.stButton > button:hover{

    background:#FFD700;
    color:black;

}


.title{

    text-align:center;
    color:#FFD700;
    font-size:48px;
    font-weight:800;

}


.card{

    background:rgba(255,255,255,0.08);
    padding:20px;
    border-radius:20px;
    border:1px solid rgba(212,175,55,0.5);

}

</style>

""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    "assets/logo.png",
    use_container_width=True
)


st.sidebar.title(
    "☕ Brew & Bean Coffee"
)


page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📖 Menu",
        "🛒 Cart",
        "💳 Payment",
        "📝 Signup",
        "👤 My Account",
        "📞 Contact",
        "👨‍💼 Admin"
        
    ]
)


st.sidebar.divider()


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
        "<h1 class='title'>☕ Brew & Bean Coffee</h1>",
        unsafe_allow_html=True
    )


    st.markdown("""
    <div class="card">

    Welcome to Brew & Bean Coffee ☕

    Fresh Coffee | Premium Taste | Fast Service

    </div>
    """,
    unsafe_allow_html=True)



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
                # ==========================================
# EDIT / DELETE MENU PRODUCTS
# ==========================================

        st.divider()
        st.subheader("✏️ Edit / Delete Menu")

        menu_response = (
                supabase
                .table("menu")
                .select("*")
                .order("id")
                .execute()
            )

        if menu_response.data:

                menu_df = pd.DataFrame(menu_response.data)

                selected = st.selectbox(
                    "Select Coffee",
                    menu_df["name"]
                )

                product = menu_df[
                    menu_df["name"] == selected
            ].iloc[0]

                new_name = st.text_input(
                    "Coffee Name",
                    value=product["name"]
                )

                new_price = st.number_input(
                    "Price",
                    min_value=1,
                    value=int(product["price"])
                )

                new_image = st.file_uploader(
                    "Change Image (Optional)",
                    type=["png","jpg","jpeg"],
                    key="edit_image"
                )

                col1, col2 = st.columns(2)

    # ===========================
    # UPDATE
    # ===========================
        with col1:

            if st.button("💾 Update Product"):

             image_url = product["image"]

            if new_image is not None:

             file_name = str(uuid.uuid4()) + ".jpg"

             image_bytes = new_image.read()

             supabase.storage \
            .from_("coffee-images") \
            .upload(
                file_name,
                image_bytes,
                {
                    "content-type": "image/jpeg"
                }
            )

             image_url = (
             supabase.storage
            .from_("coffee-images")
            .get_public_url(file_name)
            )

             supabase.table("menu").update({

            "name": new_name,
            "price": new_price,
            "image": image_url

            }).eq("id", product["id"]).execute()

            st.success("✅ Product Updated")

            st.rerun()
        
          # ===========================
    # DELETE
    # ===========================

        with col2:

            if st.button("🗑 Delete Product"):

             (
            supabase
            .table("menu")
            .delete()
            .eq("id", product["id"])
            .execute()
            )

            st.success("🗑 Product Deleted")
            st.rerun()

    else:


         st.error(
            "❌ Admin Login Required"
         )   