<?php
// include('../includes/connect.php');
session_start();

// if(isset($_GET['pay']))
// {


 $apiKey="rzp_test_2T3oCiywzSU33L";

// $ids=$_GET['pay'];
// $sql= "SELECT estimate_price FROM tbl_service where service_id='$ids'";  
// $result = mysqli_query($dbc,$sql);

// if ($result->num_rows > 0) {
//     while ($row = $result->fetch_array()) { 
//         $x=$row['estimate_price'];
//     }}


$x=$_GET['amount'];
// }
?>
<!-- <form action="houseowner_index.php?home" method="POST"> -->
    <form action="" method="post">
<script

    src="https://checkout.razorpay.com/v1/checkout.js"
    data-key="<?php echo $apiKey; ?>" // Enter the Test API Key ID generated from Dashboard → Settings → API Keys
    data-amount="<?php echo  $x * 100;?>" // Amount is in currency subunits. Hence, 29935 refers to 29935 paise or ₹299.35.
    data-currency="INR"// You can accept international payments by changing the currency code. Contact our Support Team to enable International for your account
    data-id="order_CgmcjRh9ti2lP7"// Replace with the order_id generated by you in the backend.
    data-buttontext="Pay Now"
    data-name="WoodCraft"
    data-description="Loving the Staycation vibes!"
    data-image="https://thumbs.dreamstime.com/b/house-tree-logo-real-estate-image-vector-design-graphic-symbol-template-105126143.jpg"
    data-prefill.name=""
    data-prefill.email=""
    data-theme.color=" #5F9EA0"
>alert('test');</script>
<input type="hidden" custom="Hidden Element" name="hidden" class="btn btn-primary">
<a href="http://127.0.0.1:8000/usrhommenu/">BACK TO HOME</a>
<style>
    .razorpay-payment-button{
        margin-left: 35%;
        margin-top:20%;
        width:400px;
        height:130px;
        background-color: #0DCAF0;
        color: white;
        font-size: 18px;padding: 8px 10px;font-weight: bold;
        border-radius: 12px; border: none;text-align: center; left:1500px;
    }
</style>
</form>