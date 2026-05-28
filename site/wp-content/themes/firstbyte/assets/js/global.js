;
(function ($) {

        /*
        let responsiveSliderSettings = {
            rows: 0,
            slidesToShow: 2,
            dots: true,
        };
        let $responsiveSlider = $('.selector');
         */

        // Scripts which runs after DOM load
        var scrollOut;
        $(function () {

            $(document).ready(function () {
				
                function newGridBlockSlider() {
                    if ($(window).width() <= 800) {

                        $('.grid-blocks-main').slick({
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: true,
                            autoplay: true,
                        });
                    }else{
                        if ($('.grid-blocks-main').hasClass('slick-initialized')) {
                            $('.grid-blocks-main').slick('unslick');
                        }
                    }
                }

                newGridBlockSlider();

                function initializeSlickFeaturedProjects() {
                    if ($(window).width() <= 640) {
                        $('.central-main-block').slick({
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            dots: false,
                            infinite: true,
                            arrows: false,
                            autoplay: true,
                            centerMode: true,
                        });

                        $('.steps-items').slick({
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            dots: false,
                            infinite: true,
                            arrows: true,
                            autoplay: true,
                        });


                    } else {
                        if ($('.central-main-block').hasClass('slick-initialized')) {
                            $('.central-main-block').slick('unslick');
                        }

                        if ($('.steps-items').hasClass('slick-initialized')) {
                            $('.steps-items').slick('unslick');
                        }
                    }
                }

                initializeSlickFeaturedProjects();

                $(window).on('resize', function () {
                    initializeSlickFeaturedProjects();
                    newGridBlockSlider();

                });

                const Footer = document.querySelector('.footer');
                if (Footer){
                    let footerMenuDesc = document.querySelector('#menu-footer-menu');
                    if (footerMenuDesc){
                        let menuFooterItems = document.querySelectorAll('#menu-footer-menu li');
                        if (menuFooterItems.length >= 1){
                            let lastItemMenu = menuFooterItems.item(menuFooterItems.length -1);
                            let link =  lastItemMenu.querySelector('a');
                            link.setAttribute('target', '_blank')
                        }
                    }
                }

                $('.testy-block-right-testimonials').slick({
                    infinite: true,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    autoplay: true,
                    autoplaySpeed: 2000,
                    arrows: true,
                    dots: true,
                });
				
                $('.work-main-posts').slick({
                    infinite: true,
                    slidesToShow: 6,
                    slidesToScroll: 1,
                    autoplay: true,
                    autoplaySpeed: 2000,
                    arrows: true,
                    variableWidth: true,
                    dots: false,
                    appendArrows: $('.custom-arrows'),
                    prevArrow: '<button id="prev" class="prev" type="button"></button>',
                    nextArrow: '<button id="next" class="next" type="button"></button>',
                    responsive: [

                        {
                            breakpoint: 1024,
                            settings: {
                                slidesToShow: 2,
                                slidesToScroll: 1
                            }
                        },
                        {
                            breakpoint: 641,
                            settings: {
                                slidesToShow: 1,
                                slidesToScroll: 1
                            }
                        },
                    ]
                });


                const Hero = document.querySelector('section.hero');

                if (Hero) {
                    let heroArrow = Hero.querySelector('.hero-arrow a');
                    if (heroArrow) {

                        if (window.innerWidth <= 640){
                            heroArrow.addEventListener('click', e => {
                                e.preventDefault();
                                let nextSection = Hero.nextElementSibling.nextElementSibling;
                                nextSection.scrollIntoView({
                                    behavior: 'smooth',
                                    block: 'center',
                                });
                            });
                        }else{
                            heroArrow.addEventListener('click', e => {
                                e.preventDefault();
                                let nextSection = Hero.nextElementSibling;
                                nextSection.scrollIntoView({
                                    behavior: 'smooth',
                                    block: 'center',
                                });
                            });
                        }


                    }

                }


                const SectionGet = document.querySelector('section.get');
                if (SectionGet) {


                    let formDef = document.querySelector('.get-block-left-form');
                    if (formDef) {

                        document.querySelectorAll('.gfield--type-text').forEach(group => {
                            const input = group.querySelector('.gfield input');
                            const label = group.querySelector('.gfield label');

                            if (input && label) {
                                input.addEventListener('focus', () => {
                                    label.classList.add('focused');
                                });

                                input.addEventListener('blur', () => {
                                    if (input.value === '') {
                                        label.classList.remove('focused');
                                    }
                                });
                            }
                        });

                        document.querySelectorAll('.gfield--type-email').forEach(group => {
                            const input = group.querySelector('.gfield input');
                            const label = group.querySelector('.gfield label');

                            if (input && label) {
                                input.addEventListener('focus', () => {
                                    label.classList.add('focused');
                                });

                                input.addEventListener('blur', () => {
                                    if (input.value === '') {
                                        label.classList.remove('focused');
                                    }
                                });
                            }
                        });

                        document.querySelectorAll('.gfield--type-textarea').forEach(group => {
                            const input = group.querySelector('.gfield textarea');
                            const label = group.querySelector('.gfield label');

                            if (input && label) {
                                input.addEventListener('focus', () => {
                                    label.classList.add('focused');
                                });

                                input.addEventListener('blur', () => {
                                    if (input.value === '') {
                                        label.classList.remove('focused');
                                    }
                                });
                            }
                        });
                    }
                }
                $('.info_slider-main-rep').slick({
                    infinite: true,
                    slidesToShow: 6,
                    slidesToScroll: 1,
                    autoplay: true,
                    autoplaySpeed: 2000,
                    arrows: false,
                    dots: false,
                    pauseOnHover:true,
                    mobileFirst: false,
                    responsive: [
                        {
                            breakpoint: 1900,
                            settings: {
                                // infinite: true,
                                slidesToShow: 4,
                                slidesToScroll: 1
                            }
                        },

                        {
                            breakpoint: 801,
                            settings: {
                                // infinite: true,
                                slidesToShow: 2,
                                slidesToScroll: 1
                            }
                        },
                        {
                            breakpoint: 641,
                            settings: {
                                // infinite: true,
                                slidesToShow: 1,
                                slidesToScroll: 1
                            }
                        },
                    ]
                });
				
// 				console.log('test');
				
// 				$(document).on('gform_confirmation_loaded', function(event, formId){
// 					if(formId == 1) { 
// 						setTimeout(function() {
// 							$('#input_1_1').focus();
// 						}, 100);
// 					}
// 				});
				
            });
			
			
            // Init LazyLoad
            var lazyLoadInstance = new LazyLoad({
                elements_selector: 'img[data-lazy-src],.pre-lazyload,[data-pre-lazyload],video:not([src]):not([data-lazy-src]),video[data-lazy-src]',
                data_src: "lazy-src",
                data_srcset: "lazy-srcset",
                data_sizes: "lazy-sizes",
                skip_invisible: false,
                class_loading: "lazyloading",
                class_loaded: "lazyloaded",
            });
            // Add tracking on adding any new nodes to body to update lazyload for the new images (AJAX for example)
            window.addEventListener('LazyLoad::Initialized', function (e) {
                // Get the instance and puts it in the lazyLoadInstance variable
                if (window.MutationObserver) {
                    var observer = new MutationObserver(function (mutations) {
                        mutations.forEach(function (mutation) {
                            mutation.addedNodes.forEach(function (node) {
                                if (typeof node.getElementsByTagName !== 'function') {
                                    return;
                                }
                                imgs = node.getElementsByTagName('img');
                                if (0 === imgs.length) {
                                    return;
                                }
                                lazyLoadInstance.update();
                            });
                        });
                    });
                    var b = document.getElementsByTagName("body")[0];
                    var config = {childList: true, subtree: true};
                    observer.observe(b, config);
                }
            }, false);

            // Load all images in slider after init
            $(document).on("init", ".slick-slider", function (e, slick) {
                lazyLoadInstance.loadAll(slick.$slider[0].getElementsByTagName('img'));
            });

            /*
            // responsiveSliderSettings - Settings for slider on responsive. Create this variable in the top of this file before $(document).ready()
            reinitSlickOnResize($responsiveSlider, responsiveSliderSettings, 641)
             */

            // Detect element appearance in viewport
            scrollOut = ScrollOut({
                offset: function (el) {
                    let bodyRect = document.body.getBoundingClientRect();
                    let rect = el.getBoundingClientRect();
                    let offset = rect.top - bodyRect.top - window.innerHeight;
                    return offset + 50;
                },
                targets: '.acf-map,[data-scroll]',
                once: true,
                onShown: function (element) {
                    if ($(element).is('.ease-order')) {
                        $(element).find('.ease-order__item').each(function (i) {
                            var $this = $(this);
                            $(this).attr('data-scroll', '');
                            window.setTimeout(function () {
                                $this.attr('data-scroll', 'in');
                            }, 300 * i);
                        });
                    }
                    if ($(element).is('.acf-map')) {
                        render_map($(element));
                    }
                }
            });


            // Init parallax
            if (typeof $.fn.jarallax !== 'undefined') {
                $('.jarallax').jarallax({
                    speed: 0.5,
                });

                $('.jarallax-inline').jarallax({
                    speed: 0.5,
                    keepImg: true,
                    onInit: function () {
                        lazyLoadInstance.update();
                    }
                });
            }

            //Remove placeholder on click
            $('input, textarea').each(function () {
                removeInputPlaceholderOnFocus(this);
            });

            //Make elements equal height
            if (typeof $.fn.matchHeight !== 'undefined') {
                $('.matchHeight').matchHeight();
            }

            // Add fancybox to images
            $('.gallery-item').find('a[href$="jpg"], a[href$="png"], a[href$="gif"]').attr('rel', 'gallery').attr('data-fancybox', 'gallery');
            $('a[rel*="album"], .fancybox, a[href$="jpg"], a[href$="png"], a[href$="gif"]').fancybox({});

            /**
             * Scroll to Gravity Form confirmation message after form submit
             */
            $(document).on('gform_confirmation_loaded', function (event, formId) {
                var $target = $('#gform_confirmation_wrapper_' + formId);
                smoothScrollTo($target);
            });

            // Init Jquery UI select
            $("select").not("#billing_state, #shipping_state, #billing_country, #shipping_country, [class*='woocommerce'], #product_cat, #rating").each(function () {
                initSelect2(this);
            });

            $(document).on('gform_post_render', function (event, form_id, current_page) {
                const $form = $("#gform_" + form_id)
                $form.find("select").each(function () {
                    initSelect2(this);
                });

                $form.find("input, textarea").each(function () {
                    removeInputPlaceholderOnFocus(this);
                });
            });

            $(document).on('click', '.s-qty-dec,.s-qty-inc', function () {
                var $numberInput = $(this).closest('.quantity').find('input'),
                    action = $(this).is('.s-qty-inc') ? 'stepUp' : 'stepDown';
                $numberInput[0][action]();
                $numberInput.trigger('change');
            });

            /**
             * Update lazyload images and reinit select on cart/checkout update
             */
            $(document).on('updated_wc_div', function () {
                lazyLoadInstance.loadAll();
                $('body').find('div.woocommerce').find('select').each(function () {
                    initSelect2(this);
                });
            });

            /**
             * Hide gravity forms required field message on data input
             */
            $('body').on('change keyup', '.gfield input, .gfield textarea, .gfield select', function () {
                var $field = $(this).closest('.gfield');
                if ($field.hasClass('gfield_error') && $(this).val().length) {
                    $field.find('.validation_message').hide();
                } else if ($field.hasClass('gfield_error') && !$(this).val().length) {
                    $field.find('.validation_message').show();
                }
            });

            /**
             * Add `is-active` class to menu-icon button on Responsive menu toggle
             * And remove it on breakpoint change
             */
            $(window).on('toggled.zf.responsiveToggle', function () {
                $('.menu-icon').toggleClass('is-active');
            }).on('changed.zf.mediaquery', function (e, value) {
                $('.menu-icon').removeClass('is-active');
            });

            /**
             * Close responsive menu on orientation change
             */
            $(window).on('orientationchange', function () {
                setTimeout(function () {
                    if ($('.menu-icon').hasClass('is-active') && window.innerWidth < 641) {
                        $('[data-responsive-toggle="main-menu"]').foundation('toggleMenu')
                    }
                }, 200);
            });

            resizeVideo();

            // Share post popup
            $('.js-share-link').click(function (e) {
                e.preventDefault();
                var wpWidth = $(window).width(), wpHeight = $(window).height();
                window.open($(this).attr('href'), 'Share', "top=" + (wpHeight - 400) / 2 + ",left=" + (wpWidth - 600) / 2 + ",width=600,height=400");
            });

        });


// Scripts which runs after all elements load

        $(window).on('load', function () {

            if (typeof scrollOut !== "undefined") {
                scrollOut.update();
            }

            //jQuery code goes here
            if ($('.preloader').length) {
                $('.preloader').addClass('preloader--hidden');
            }

        });

// Scripts which runs at window resize

        let resizeVideoCallback = debounce(resizeVideo, 200);
// let resizeSliderCallback = debounce( reinitSlickOnResize, 200 );
        $(window).on('resize', function () {

            //jQuery code goes here
            resizeVideoCallback();

            /*
            resizeSliderCallback( $responsiveSlider, responsiveSliderSettings, 641 );
            */


        });

// Scripts which runs on scrolling

        $(window).on('scroll', function () {

            //jQuery code goes here

        });

        /*
         *  This function will render a Google Map onto the selected jQuery element
         */

        function render_map($el) {
            // var
            var $markers = $el.find('.marker');
            // var styles = Here should be styles for Google Maps from https://snazzymaps.com/explore ; // Uncomment for map styling

            // vars
            var args = {
                zoom: 16,
                center: new google.maps.LatLng(0, 0),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                scrollwheel: false,
                // styles : styles // Uncomment for map styling
            };

            // create map
            var map = new google.maps.Map($el[0], args);

            // add a markers reference
            map.markers = [];

            // add markers
            $markers.each(function () {
                add_marker($(this), map);
            });

            // center map
            center_map(map);
        }

        /*
         *  This function will add a marker to the selected Google Map
         */

        var infowindow;

        function add_marker($marker, map) {
            // var
            var latlng = new google.maps.LatLng($marker.attr('data-lat'), $marker.attr('data-lng'));

            // create marker
            var marker = new google.maps.Marker({
                position: latlng,
                map: map,
                //icon: $marker.data('marker-icon') //uncomment if you use custom marker
            });

            // add to array
            map.markers.push(marker);

            // if marker contains HTML, add it to an infoWindow
            if ($.trim($marker.html())) {
                // create info window
                infowindow = new google.maps.InfoWindow();

                // show info window when marker is clicked
                google.maps.event.addListener(marker, 'click', function () {
                    // Close previously opened infowindow, fill with new content and open it
                    infowindow.close();
                    infowindow.setContent($marker.html());
                    infowindow.open(map, marker);
                });
            }
        }

        /*
        *  This function will center the map, showing all markers attached to this map
        */

        function center_map(map) {
            // vars
            var bounds = new google.maps.LatLngBounds();

            // loop through all markers and create bounds
            $.each(map.markers, function (i, marker) {
                var latlng = new google.maps.LatLng(marker.position.lat(), marker.position.lng());
                bounds.extend(latlng);
            });

            // only 1 marker?
            if (map.markers.length == 1) {
                // set center of map
                map.setCenter(bounds.getCenter());
            } else {
                // fit to bounds
                map.fitBounds(bounds);
            }
        }

        /**
         * Helper functions
         */

        function debounce(callback, time) {
            var timeout;

            return function () {
                var context = this;
                var args = arguments;
                if (timeout) {
                    clearTimeout(timeout);
                }
                timeout = setTimeout(function () {
                    timeout = null;
                    callback.apply(context, args);
                }, time);
            }
        }

        function handleFirstTab(e) {
            var key = e.key || e.keyCode;
            if (key === 'Tab' || key === '9') {
                $('body').removeClass('no-outline');

                window.removeEventListener('keydown', handleFirstTab);
                window.addEventListener('mousedown', handleMouseDownOnce);
            }
        }

        function handleMouseDownOnce() {
            $('body').addClass('no-outline');

            window.removeEventListener('mousedown', handleMouseDownOnce);
            window.addEventListener('keydown', handleFirstTab);
        }

        window.addEventListener('keydown', handleFirstTab);

// Fit slide video background to video holder
        function resizeVideo() {
            var $holder = $(".video-holder");
            $holder.each(function () {
                var $that = $(this);
                var ratio = $that.data("ratio") ? $that.data("ratio") : "16:9",
                    width = parseFloat(ratio.split(":")[0]),
                    height = parseFloat(ratio.split(":")[1]);
                $that.find(".video-holder__media").each(function () {
                    if ($that.width() / width > $that.height() / height) {
                        $(this).css({"width": "100%", "height": "auto"});
                    } else {
                        $(this).css({"width": $that.height() * width / height, "height": "100%"});
                    }
                });
            });
        }

// Init Select2 plugin
        function initSelect2(elem) {
            var $field = $(elem);
            var $gfield = $field.closest(".gfield");
            var $countryBox = $field.closest('.ginput_address_country,.gfield_time_ampm');
            var args = {}
            if ($countryBox.length) {
                args.dropdownParent = $countryBox;
            } else if ($gfield.length) {
                args.dropdownParent = $gfield;
            }

            $field.select2(args);
        }

        function removeInputPlaceholderOnFocus(el) {
            $(el).data("holder", $(el).attr("placeholder"));

            $(el).on("focusin", function () {
                $(el).attr("placeholder", "");
            });

            $(el).on("focusout", function () {
                $(el).attr("placeholder", $(el).data("holder"));
            });
        }

        /**
         * Init slick slider on smaller screens, And destroy it on desktop
         */
        function reinitSlickOnResize($slider, settings, breakpoint) {
            if (window.innerWidth >= breakpoint) {
                if ($slider.hasClass("slick-initialized")) {
                    $slider.slick("unslick");
                }
            } else {
                if (!$slider.hasClass("slick-initialized")) {
                    $slider.slick(settings);
                }
            }
        }

        /**
         * Smooth scroll to target
         */
        function smoothScrollTo($target, offset) {
            offset = typeof offset == "undefined" ? 0 : offset;
            $("html, body").animate({
                scrollTop: $target.offset().top - 50 - offset,
            }, 500);
            $target.focus();
            if ($target.is(":focus")) { // Checking if the target was focused
                return false;
            } else {
                $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                $target.focus(); // Set focus again
            }
        }

    }
    (jQuery)
)
;