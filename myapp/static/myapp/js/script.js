const barmenu= document.getElementById('bar');
const navbar= document.getElementById('nav');
const crossbar= document.getElementById('cross');
if(bar){
    barmenu.addEventListener('click', ()=>{
        navbar.classList.add('active');
    })
}

if(cross){
    crossbar.addEventListener('click',()=>{
        navbar.classList.remove('active');
    })
}


$('.plus-cart').click(function(){
    var eml=this.parentNode.children[2]
    var id=$(this).attr("pid").toString();
    console.log("pid =",id)    //for my understanding in console
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            product_id:id
        },
        success:function(data){
            console.log("data: ",data)
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var eml=this.parentNode.children[2]
    var id=$(this).attr("pid").toString();
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            product_id:id
        },
        success:function(data){
            console.log("data: ",data)
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})



$('.remove-cart').click(function(){
    var eml=this
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            product_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()   //removing class="row" means 4th parent node in div
        }
    })
})
  
  