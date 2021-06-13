class TemplateFormatter {
    constructor(element_template, context) {
        this.element_template = element_template;
        this.format(context);
    }

    format(context) {
        for (const key in context) {
            console.log(`{${key}}`)
            this.element_template = this.element_template.replaceAll(`{${key}}`, context[key]);
        }
    }

    getJqueryElement() {
        return $(this.element_template);
    }
}

// {slug} , {product_photo}, {product_name}
const T_product_cart = `
<a href="javascript:void(0);" data="{slug}" class="sl__plist__pcard">
    <div class="sl__plist__pcard-box">
        <div class="sl__plist__pcard-img"><img src="{product_photo}" alt="*">
        </div>
        <div class="sl__plist__pcard-title">{product_name}</div>
    </div>
</a>`;

// {msg}
const T_product_notfound_box = `
<div style="color: black; padding: 10px 15px; border-radius: 15px; background-color: rgb(240, 240, 240);">
    {msg}
</div>
`;

// {product_photo} {product_name} {brand} {alternative_name[1-4]} {stock_class} {original_class}
// {price} {currency}
const T_product_details = `<div class="sl__pdetal__informations">
<div class="sl__pdetail__informations-img">
    <img src="{product_photo}" alt="***">
</div>
<div class="sl__pdetail__informations-list">
    <div class="sl__pdetail__informations-title">{product_name}</div>
    <div class="sl__pdetail__informations-description">{brand}</div>
</div>
</div>
<!-- Alternative Name -->
<div class="sl__pdetail__anl">
<div class="sl__pdetail__anl-title">alternative name</div>
<div class="sl__pdetail__anl-list">
    <div class="sl__pdetail__anl-item">{alternative_name_1}</div>
    <div class="sl__pdetail__anl-item">{alternative_name_2}</div>
    <div class="sl__pdetail__anl-item">{alternative_name_3}</div>
    <div class="sl__pdetail__anl-item">{alternative_name_4}</div>
</div>
</div>
<!-- Origianl Or Stock -->
<div class="sl__pdetail__oos original">
<div class="sl__pdetail__oos-box">
    <a href="#" class="{stock_class}" >stock</a>
    <a href="#" class="{original_class}">original</a>
</div>
</div>
<div class="sl__pdetail__price">
<div class="sl__pdetail__price-title">قیمت</div>
<div class="sl__pdetail__price-number">{price} {currency}</div>
</div>`;


const T_loader = `
<div class="loader-dialog">
    <div class="loader"></div>
</div>
`;