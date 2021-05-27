let closeMenu = () => {
    let element = document.querySelector(".nav__items");
    element.classList.remove("open");
};

let openMenu = () => {
    let element = document.querySelector(".nav__items");
    element.classList.add("open");
}

let button = document.querySelector(".nav__openner");
button.addEventListener("click", openMenu);



let close = document.querySelector(".times");
close.addEventListener("click", closeMenu);

const search = (keyword) => {
    $.get("/search", { "keyword": keyword })
        .done((data) => {
            $(".sl").css('display', 'flex');
            data.results.forEach(element => {
                $(".sl__plist-box").append(`<a href="javascript:void(0);" data="${element.slug}" class="sl__plist__pcard">
                <div class="sl__plist__pcard-box">
                    <div class="sl__plist__pcard-img"><img src="${element.product_photo}" alt="*">
                    </div>
                    <div class="sl__plist__pcard-title">${element.product_name}</div>
                </div>
            </a>`)
            });
            $(".sl__plist__pcard:first").addClass('active');
        })
        .fail(() => {
            console.log("fail")
        });

};
const getProduct = slug => {
    return new Promise((resolve, reject) => {
        $.get("/get_product", { "slug": slug })
            .done((data) => {
                data = data.results;
                resolve(data);
            })
            .fail(() => {
                reject("fail")
            });
    });

};
$('#navSearch').submit(function(e) {
    e.preventDefault();
    search($("#keyword").val())
});

const addToCart = (slug, qty) => {
    cat = JSON.parse(localStorage.getItem('items'));
    if (!cat) {
        cat = [];
        item = {};
        item[slug] = qty;
        cat.push(item)
    } else {
        found = false;
        for (i in cat) {
            if (Object.keys(cat[i])[0] == slug) {
                item = {};
                item[slug] = qty;
                cat[i] = item;
                found = true;
            }
        }
        if (!found) {
            item = {};
            item[slug] = qty;
            cat.push(item);
        }
    }
    localStorage.setItem('items', JSON.stringify(cat));
    $("#cartItems").html(cat.length)
};