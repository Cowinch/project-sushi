//thise code is used to ask the user if they're sure they want to delete something
var elems = document.getElementsByClassName('confirmation');
    var confirmIt = function (e) {//this code comes from https://stackoverflow.com/questions/10462839/how-to-display-a-confirmation-dialog-when-clicking-an-a-link
        if (!confirm('Are you sure about that?')) e.preventDefault();
    };
    for (var i = 0, l = elems.length; i < l; i++) {
        elems[i].addEventListener('click', confirmIt, false);
    }

let select=document.getElementById('select')
let categoryList=document.getElementById('category-list')
let selectText=document.getElementById('select-text')
let options=document.getElementsByClassName('options')
let inputField=document.getElementById('input-field')
let restaurantList=document.getElementById('restaurant-list')
let sushiList=document.querySelector('#sushi-list')
let allList=document.querySelector('#all-list')
select.onclick=function(){
    categoryList.classList.toggle('open');
}
for(option of options){
    option.onclick=function(){
        selectText.innerHTML=this.innerHTML;
        inputField.placeholder='Search ' + selectText.innerHTML;
    }
}

function searchRestaurant() {
    let selection=document.querySelector('#select-text').innerText.toLowerCase();
    let input = document.getElementById('input-field').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName(selection);
    
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="list-item";                 
        }
    }
    if(selection=='restaurants'){
        if (input.length>=1){
            console.log(input.length)
            restaurantList.classList.add('display')
        }
        else{
            restaurantList.classList.remove('display')
        }
    }
    if(selection=='sushi'){
        if (input.length>=1){
            console.log(input.length)
            sushiList.classList.add('display')
        }
        else{
            sushiList.classList.remove('display')
        }
    }
    if(selection=='all'){
        if (input.length>=1){
            console.log(input.length)
            allList.classList.add('display')
        }
        else{
            allList.classList.remove('display')
        }
    }
}

function profilePictureUpdate(){
    let profilePicture=document.querySelector('.pfp-box')
    profilePicture.classList.toggle('display-pfp')

}

function addFriend(){
    let friendInput=document.querySelector('.add-input')
    friendInput.classList.toggle('display-input')
}

let friendList=document.querySelector('#friends-list')
function searchFriends(){
    let input = document.getElementById('add-friend').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('friends');
    
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="list-item";                 
        }
    }

    if (input.length>=1){
        console.log(input.length)
        friendList.classList.add('display-friends')
    }
    else{
        friendList.classList.remove('display-friends')
    }
}
