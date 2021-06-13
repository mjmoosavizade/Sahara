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
            toggle_search();
            $(".sl").css('display', 'flex');
            $(".sl__plist-box").empty(); // clear previous search results
            $(".sl__plist__pnr-num").text(data.results.length);
            if (!data.results.length) {
                let $msg = new TemplateFormatter(T_product_notfound_box, {
                    msg: "محصولی یافت نشد"
                }).getJqueryElement();
                $(".sl__plist-box").addClass("flex-content-center");
                $(".sl__plist-box").append($msg);
                return;
            }
            data.results.forEach((element, i) => {
                let $cart = new TemplateFormatter(T_product_cart, {
                    slug: element.slug,
                    product_photo: element.product_photo,
                    product_name: element.product_name
                }).getJqueryElement();
                $(".sl__plist-box").append($cart);
                if (i == 0)
                    selectProduct($cart[0]);
            });
            $("sl__plist__pnr-num").text(data.results.length);
            $(".sl__plist-box").removeClass("flex-content-center");
            $(".sl__plist__pcard:first").addClass('active');
        })
        .fail(() => {
            console.log("fail")
        });
};

const toggle_search = () => {
    $(".sl").fadeToggle(200);
    if ($(".sl").css("display") == "flex") {
        $(".sl__pdetail-box").empty();
    }
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

const search_hanlder = event => {
    event.preventDefault();
    search($("#keyword").val());
}

const selectProduct = product_element => {
    $(product_element).addClass('active');
    $(product_element).siblings().removeClass("active");
    getProduct(product_element.getAttribute('data')).then( data =>{
        stockClass = '';
        originalClass = '';
        if (data.type == 'Stock') {
            stockClass = 'sl__pdetail__oos-original'
            originalClass = 'sl__pdetail__oos-stock'
        } else {
            originalClass = 'sl__pdetail__oos-original'
            stockClass = 'sl__pdetail__oos-stock'
        }
        $(".sl__pdetail-box").empty();
        $(".sl__pdetail-box").append(`<div class="sl__pdetail__informations">
                    <div class="sl__pdetail__informations-img">
                        <img src="${data.product_photo}" alt="***">
                    </div>
                    <div class="sl__pdetail__informations-list">
                        <div class="sl__pdetail__informations-title">${data.product_name}</div>
                        <div class="sl__pdetail__informations-description">${data.brand}</div>
                    </div>
                </div>
                <!-- Alternative Name -->
                <div class="sl__pdetail__anl">
                    <div class="sl__pdetail__anl-title">alternative name</div>
                    <div class="sl__pdetail__anl-list">
                        <div class="sl__pdetail__anl-item">${data.alternative_name_1}</div>
                        <div class="sl__pdetail__anl-item">${data.alternative_name_2}</div>
                        <div class="sl__pdetail__anl-item">${data.alternative_name_3}</div>
                        <div class="sl__pdetail__anl-item">${data.alternative_name_4}</div>
                    </div>
                </div>
                <!-- Origianl Or Stock -->
                <div class="sl__pdetail__oos original">
                    <div class="sl__pdetail__oos-box">
                        <a href="#" class="${ stockClass }" >stock</a>
                        <a href="#" class="${ originalClass }">original</a>
                    </div>
                </div>
                <div class="sl__pdetail__price">
                    <div class="sl__pdetail__price-title">قیمت</div>
                    <div class="sl__pdetail__price-number">${data.price} ${data.currency}</div>
                </div>`);
    });
}

const searchMostVisitedProducts = keyword => {
    if (!keyword) return;
    let nomatch_found = true;
    $(".mvp-name").each((i, product) => {
        const product_name = $(product).text();
        console.log(product_name);
        if (!product_name.includes(keyword) && !$(product).next().text().includes(keyword))
            $(product).parent().fadeOut(300);
        else {
            nomatch_found = false;
            $(product).parent().fadeIn(300);
        }
    });
    if (nomatch_found) {
        $("#nfound-box").fadeIn(300);
    }
    else {
        $("#nfound-box").fadeOut(300);
    }
}
$("#mvs-search-btn").click(event => {
    event.preventDefault();
    searchMostVisitedProducts($("#mvs-search-input").val());
});
$("#mvs-search-input").keypress(event => {
    if (event.keycode == 13) {
        searchMostVisitedProducts($("#mvs-search-input").val());
    }
});

$('#navSearch').submit(search_hanlder);
$('#search-btn').click(search_hanlder);
$('.sl').click(search_hanlder);
$('.sl-box').click(event=>event.stopPropagation());

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
    $("#cartItems").html(cat.length);
};