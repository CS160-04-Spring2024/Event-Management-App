    $(document).ready(function () {
        // Add click event listener to checkboxes
        $('.form-check-input').change(function () {
            var checkboxId = $(this).attr('for');
            var labelForCheckbox = $('label[id="' + checkboxId + '"]');

            if ($(this).is(':checked')) {
                labelForCheckbox.addClass('checked');
            } else {
                labelForCheckbox.removeClass('checked');
            }
            
            $('input[name="selected_tags"]').change(function () {
                var selectedTags = $('input[name="selected_tags"]:checked').map(function () {
                    return this.value;
                }).get();
                $('#selectedTagsInput').val(selectedTags.join(','));
            });
        });
        
            $('#sidebarCollapse').on('click', function () {
            $('#sidebar').toggleClass('active');
        });
        checkSelectedValue();
    });


      // Check the selected value on change
        $('#userType').change(function () {
            checkSelectedValue();
        });

        function checkSelectedValue() {
            var selectedValue = $('#userType').val();
            if (selectedValue === '2') {
                $('#clubSelect').show();
            } else if (selectedValue === '1') {
                $('#clubSelect').hide();
            }
        }


    document.getElementById('club').addEventListener('change', function () {
        var selectedOption = document.querySelector('#club_list option[value="' + this.value + '"]');
        if (selectedOption) {
            var selectedId = selectedOption.getAttribute('data-id');
            document.getElementById('selectedClubId').value = selectedId;
        }
    });

    document.getElementById('location').addEventListener('change', function () {
        var selectedOption = document.querySelector('#locationList option[value="' + this.value + '"]');
        if (selectedOption) {
            var selectedId = selectedOption.getAttribute('data-id');
            document.getElementById('selectedLocationId').value = selectedId;
        }
    });