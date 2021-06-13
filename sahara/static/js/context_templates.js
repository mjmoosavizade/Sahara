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