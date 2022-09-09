var updateBtns = document.getElementsByClassName('update-cart');
for(var i=0 ; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('product: ', productID,'action:', action)
        console.log('USER: ', user)
        if( user === 'AnonymousUser'){
            addCookieItem(productID, action)

        }else{
            updateUserOrder(productID, action)

        }
    })
}


function addCookieItem(productID, action){
    console.log('User is not not authenticated')

    if (action == 'add' ){
        if(cart_new[productID] == undefined){
            cart_new[productID] = {'quantity':1}
        }else{
            cart_new[productID]['quantity']+=1
        }

    }
    if(action == 'remove'){
            cart_new[productID]['quantity']-=1
            console.log(cart_new[productID]['quantity'])
            console.log('taaawa' ,cart_new[productID]['quantity'])

            if(cart_new[productID]['quantity'] <= 0){
                console.log("remove Item")
                delete cart_new[productID]
            }
    }
    console.log('cart_new: ', cart_new)

    document.cookie = 'cart_new=' + JSON.stringify(cart_new) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productID, action){
            console.log('user is logged in , sending data...')
            var url ='/update_item/'
            console.log('URL: ', url)
            console.log(csrftoken)

            fetch (url,{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken': csrftoken,
                },

                body:JSON.stringify({'productID':productID, 'action':action})

            })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                console.log('data: ',data)
                location.reload()
            });
            }


