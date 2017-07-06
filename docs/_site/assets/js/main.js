$(document).ready(function() {

    /* Build index */
    $(".doc-body").html('<div class="doc-content"><div class="content-inner">' + $(".doc-body").html() + '</div></div>');
    $(".doc-content").after('<div class="doc-sidebar hidden-xs"><nav id="doc-nav"><ul id="doc-menu" class="nav doc-menu affix-top" data-spy="affix"></ul></nav></div>');

    var back_obj = null;
    var doc_menu = $("#doc-menu");
    var children = $(".content-inner").children("h1");
    children.each(function (i, h1) {
        var anchor_name = "tocAnchor-" + i + "-0";
        h1.setAttribute("id", anchor_name);

        var curr_title = $('<li><a class="scrollto" href="#' + anchor_name + '">' + $(h1).html() + '</a></li>');
        doc_menu.append(curr_title);

        if (i > 0) {
            var curr_elem = i - 1;
            var next_element = null;

            if (children.length === i + 1) {
                next_element = $(h1).nextAll("h2");
                curr_elem += 1;
            } else {
                next_element = $(back_obj).nextUntil(h1, "h2");
            }

            if (next_element.length > 0) {
                var sub_objs = "";
                next_element.each(function (j, h2) {
                    var anchor_name_sub = "tocAnchor-" + curr_elem + "-" + j;

                    h2.setAttribute("id", anchor_name_sub);
                    sub_objs += '<li><a class="scrollto" href="#' + anchor_name_sub + '">' + $(h2).text() + '</a></li>';

                });

                curr_title.append('<ul class="nav doc-sub-menu">' + sub_objs + '</ul>');
            }


        }

        back_obj = h1;
    });

    /* ===== Affix Sidebar ===== */
    /* Ref: http://getbootstrap.com/javascript/#affix-examples */


    doc_menu.affix({
        offset: {
            top: ($('#header').outerHeight(true) + $('#doc-header').outerHeight(true)) + 45,
            bottom: ($('#footer').outerHeight(true) + $('#promo-block').outerHeight(true)) + 75
        }
    });

    /* Hack related to: https://github.com/twbs/bootstrap/issues/10236 */
    $(window).on('load resize', function() {
        $(window).trigger('scroll');
    });

    /* Activate scrollspy menu */
    $('body').scrollspy({target: '#doc-nav', offset: 100});

    /* Smooth scrolling */
    $('a.scrollto').on('click', function(e){
        //store hash
        var target = this.hash;
        e.preventDefault();
        $('body').scrollTo(target, 800, {offset: 0, 'axis':'y'});

    });


    /* ======= jQuery Responsive equal heights plugin ======= */
    /* Ref: https://github.com/liabru/jquery-match-height */

    $('.cards-wrapper-adjust .item-inner').matchHeight();
    $('#showcase .card').matchHeight();

    /* Bootstrap lightbox */
    /* Ref: http://ashleydw.github.io/lightbox/ */

    $(document).delegate('*[data-toggle="lightbox"]', 'click', function(e) {
        e.preventDefault();
        $(this).ekkoLightbox();
    });
});