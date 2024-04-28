    //$(document).ready(function () {
        // Add click event listener to checkboxes
        // $('.form-check-input-events-all').change(function () {
        //     var checkboxId = $(this).attr('id');
        //     var labelForCheckbox = $('label[for="' + checkboxId + '"]');

        //     if ($(this).is(':checked')) {
        //         labelForCheckbox.addClass('checked');
        //     } else {
        //         labelForCheckbox.removeClass('checked');
        //     }
            
        //     $('input[name="selected_tags"]').change(function () {
        //         var selectedTags = $('input[name="selected_tags"]:checked').map(function () {
        //             return this.value;
        //         }).get();
        //         $('#selectedTagsInput').val(selectedTags.join(','));
        //     });
        // });
        
        //     $('#sidebarCollapse').on('click', function () {
        //     $('#sidebar').toggleClass('active');
        // });
        // checkSelectedValue();
    //});


    //   // Check the selected value on change
    //     $('#userType').change(function () {
    //         checkSelectedValue();
    //     });

    //     function checkSelectedValue() {
    //         var selectedValue = $('#userType').val();
    //         if (selectedValue === '2') {
    //             $('#clubSelect').show();
    //         } else if (selectedValue === '1') {
    //             $('#clubSelect').hide();
    //         }
    //     }


    // document.getElementById('club').addEventListener('change', function () {
    //     var selectedOption = document.querySelector('#club_list option[value="' + this.value + '"]');
    //     if (selectedOption) {
    //         var selectedId = selectedOption.getAttribute('data-id');
    //         document.getElementById('selectedClubId').value = selectedId;
    //     }
    // });

    // document.getElementById('location').addEventListener('change', function () {
    //     var selectedOption = document.querySelector('#locationList option[value="' + this.value + '"]');
    //     if (selectedOption) {
    //         var selectedId = selectedOption.getAttribute('data-id');
    //         document.getElementById('selectedLocationId').value = selectedId;
    //     }
    // });



// An attempt at real time Dept. reading
    // let parent = document.getElementById('all_orgs').children
    // document.getElementById('dept_selector').addEventListener(
    //     'change', function() {

    //     }
    // )
    // function org_func(){
    //     var org = document.getElementById('admin_stuff').value;
    //     console.log(org);
    //     var adminInput = document.querySelector('#org');

    //     if(org == true || org == 'True' || org == 'Is Admin'){
    //         adminInput.removeAttribute('hidden');
    //     }else{
    //         adminInput.setAttribute('hidden');
    //     }

    // }
    // org_func();


    

    // look, i know this isn't optimal. my brain just can't think right now and it works
    // event listener for event carousel
    // document.addEventListener('DOMContentLoaded', function () {
    //     let multipleCardCarousel = document.querySelector("#eventRecs");

    //     if (window.matchMedia("(min-width: 768px)").matches) {
    //         let carousel = new bootstrap.Carousel(multipleCardCarousel, {
    //             interval: false, // Disable automatic sliding
    //             wrap: false, // Prevent wrapping at the end
    //         });

    //         let carouselWidth = document.querySelector(".carousel-inner").scrollWidth;
    //         let cardWidth = document.querySelector(".carousel-item").offsetWidth;
    //         let scrollPosition = 0;

    //         document.querySelector("#eventRecs .carousel-control-next").addEventListener("click", function () {
    //             if (scrollPosition < carouselWidth - cardWidth * 4) {
    //                 scrollPosition += cardWidth;
    //                 document.querySelector("#eventRecs .carousel-inner").scroll({ left: scrollPosition, behavior: 'smooth' });
    //             }
    //         });

    //         document.querySelector("#eventRecs .carousel-control-prev").addEventListener("click", function () {
    //             if (scrollPosition > 0) {
    //                 scrollPosition -= cardWidth;
    //                 document.querySelector("#eventRecs .carousel-inner").scroll({ left: scrollPosition, behavior: 'smooth' });
    //             }
    //         });
    //     }
    // });

    // // event listener for clubs carousel
    // document.addEventListener('DOMContentLoaded', function () {
    //     let multipleCardCarousel = document.querySelector("#clubRecs");

    //     if (window.matchMedia("(min-width: 768px)").matches) {
    //         let carousel = new bootstrap.Carousel(multipleCardCarousel, {
    //             interval: false, // Disable automatic sliding
    //             wrap: false, // Prevent wrapping at the end
    //         });

    //         let carouselWidth = document.querySelector(".carousel-inner").scrollWidth;
    //         let cardWidth = document.querySelector(".carousel-item").offsetWidth;
    //         let scrollPosition = 0;

    //         document.querySelector("#clubRecs .carousel-control-next").addEventListener("click", function () {
    //             if (scrollPosition < carouselWidth - cardWidth * 4) {
    //                 scrollPosition += cardWidth;
    //                 document.querySelector("#clubRecs .carousel-inner").scroll({ left: scrollPosition, behavior: 'smooth' });
    //             }
    //         });

    //         document.querySelector("#clubRecs .carousel-control-prev").addEventListener("click", function () {
    //             if (scrollPosition > 0) {
    //                 scrollPosition -= cardWidth;
    //                 document.querySelector("#clubRecs .carousel-inner").scroll({ left: scrollPosition, behavior: 'smooth' });
    //             }
    //         });
    //     }
    // });

    // // event listener for department/major events carousel
    // document.addEventListener('DOMContentLoaded', function () {
    //     let multipleCardCarousel = document.querySelector("#deptRecs");

    //     if (window.matchMedia("(min-width: 768px)").matches) {
    //         let carousel = new bootstrap.Carousel(multipleCardCarousel, {
    //             interval: false, // Disable automatic sliding
    //             wrap: false, // Prevent wrapping at the end
    //         });

    //         let carouselWidth = document.querySelector(".carousel-inner").scrollWidth;
    //         let cardWidth = document.querySelector(".carousel-item").offsetWidth;
    //         let scrollPosition = 0;

    //         document.querySelector("#deptRecs .carousel-control-next").addEventListener("click", function () {
    //             if (scrollPosition < carouselWidth - cardWidth * 4) {
    //                 scrollPosition += cardWidth;
    //                 document.querySelector("#deptRecs .carousel-inner").scroll({ left: scrollPosition, behavior: 'smooth' });
    //             }
    //         });

    //         document.querySelector("#deptRecs .carousel-control-prev").addEventListener("click", function () {
    //             if (scrollPosition > 0) {
    //                 scrollPosition -= cardWidth;
    //                 document.querySelector("#deptRecs .carousel-inner").scroll({ left: scrollPosition, behavior: 'smooth' });
    //             }
    //         });
    //     }
    // });
