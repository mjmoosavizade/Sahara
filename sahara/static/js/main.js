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

const search = (keyword, page=1, toggle=true) => {
    $.get("/search", { "keyword": keyword, 'page': page })
        .done((data) => {
            (toggle && toggle_search());
            $(".sl").css('display', 'flex');
            $(".sl__plist-box").empty(); // clear previous search results
            $(".sl__plist__pnr-num").text(data.num_products);
            if (!data.num_products) {
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
            // clear previous paginators
            $(".sl__plist__paginator-list").empty();
            for (let i=1; i<=data.num_pages; i++) {
                let $paginator = new TemplateFormatter(T_paginator, {
                    active: i==data.page_number? "active": "",
                    page_number: i,
                }).getJqueryElement();
                $paginator.click(event => {
                    // when user clicks on the paginator get the relavant page
                    event.preventDefault();
                    search(keyword, Number.parseInt(event.target.dataset.pagenum), false);
                });
                $(".sl__plist__paginator-list").append($paginator);
            }
        })
        .fail(() => {
            console.log("fail");
        })
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
    $(".sl__pdetail-box").empty();
    $(".sl__pdetail-box").append(new TemplateFormatter(T_loader, {}).getJqueryElement());
    $(".loader-dialog").fadeIn(50);
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
        $(".sl__pdetail-box").append(new TemplateFormatter(T_product_details, {
            product_photo: data.product_photo,
            product_name: data.product_name,
            brand: data.brand,
            alternative_name_1: data.alternative_name_1,
            alternative_name_2: data.alternative_name_2,
            alternative_name_3: data.alternative_name_3,
            alternative_name_4: data.alternative_name_4,
            stock_class: stockClass,
            original_class: originalClass,
            price: data.price,
            currency: data.currency,
        }).getJqueryElement());
        $(".loader-dialog").fadeOut(50);
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
$("#mvs-search-input").keyup(event => {
    console.log(event.target.value == "");
    if (event.target.value == "") {
        console.log("executed");
        $(".mvp-name").each((i, product) => {
            console.log(product);
            $(product).parent().fadeIn(300);
        });
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