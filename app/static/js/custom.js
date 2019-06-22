const address = window.location;


$(document).ready(function() {
    console.log("i am ready");

    /**
    Hide the Django message after 3 seconds.
     */
    document.querySelectorAll("#messages").forEach(function(message) {
        setTimeout(function() {
            $(message).fadeOut("slow");
        }, 3000)
    });


    // $("#ota-link,#partners-link,#review-link").click(function(e) {
    //     e.preventDefault();
    //
    //     const this_ = $(this);
    //
    //     // Get the pathname in order to refer which data is to be fetched i.e ota or partner or review, etc
    //     let pathname = this_.attr("href").split("/");
    //
    //     // get the type of data to be fetched i.e ota or partner etc
    //     const dataType = pathname[pathname.length-2];
    //     console.log(dataType);
    //
    //     // Insert the 'j' at the to match the view data
    //     // Eg- /enquiry/j/ota/  or /enquiry/j/partner
    //     pathname.splice(2, 0, "j");
    //
    //     // Complete URL to fetch the data
    //     const contentFetchURL = address.origin + pathname.join("/");
    //     console.log(contentFetchURL);
    //
    //
    //     $.ajax({
    //         url: contentFetchURL,
    //         method: "GET",
    //         success: function(data) {
    //             // Change the title of the page
    //             document.title = `S3 Infosoft - ${dataType[0].toUpperCase() + dataType.substring(1)}`;
    //
    //             // Change the address of the page
    //             window.history.pushState(data, null, this_.attr("href"));
    //             $(".container-fluid").html(data);
    //         },
    //         error: function(err) {
    //             console.log(err);
    //         }
    //     })
    // });


    /**
     * Function to check whether the URL ends with any of the list contents
     * @param {Array} suffixes - The suffixes to check
     * @param {String} string - The string in which to check
     * @returns {boolean}
     */
    function urlEndsWith(suffixes, string) {
        return suffixes.some(function(suffix) {
            return string.endsWith(suffix);
        });
    }


    if (window.innerWidth > 768 && urlEndsWith(["/ota/", "/review/", "/partner/"], address.pathname)) {
        const anchorTag = $(".nav-link.collapsed.admin");
        const divTag = $("#collapseAdmin");
        anchorTag.removeClass("collapsed");
        divTag.addClass("show");
    }
});

/**
 * Function to fetch the table contents from the API and attach them to the table.
 * @param {String} tableID - The table ID to attach the results
 * @param {String} apiPathname - The API pathname to send GET request
 * @param {Array} columns - The list of column names to attach data
 */
function fetchTableDataFromAPI(tableID, apiPathname, columns) {
    console.log("Entered the calling function");
    $.ajax({
        url: address.origin + apiPathname,
        method: "GET",
        dataType: "json",
        success: function(data) {
            $(tableID).dataTable({
                "aaData": data,
                "aaSorting": [],    // disable the initial sorting
                "columns": columns,
                "order": [[0, "desc"]],
            });
        }
    })
}


/**
 * Add the newly created enquiry data to table
 * @param {String} tableID - Table ID to attach the result
 * @param {String} apiPathname - API pathname to send POST request
 * @param {JSON} formData - Data to send to API
 */
function addNewEnquiryData(tableID, apiPathname, formData) {

    $.ajax({
        url: address.origin + apiPathname,
        method: "POST",
        data: formData,
        dataType: "json",
        success: function(data) {
            console.log("Successfully created enquiry.");
            let table = $(tableID).DataTable();
            table.row.add(data).draw();
        },
        error: function(err) {
            console.log(err);
        }
    })
}


/**
 * Function to handle the form submission and clearing of form after AJAX
 * @param {String} formID - Form ID to handle its submission
 * @param {String} tableID - tableID - Table ID to attach the result
 * @param {String} apiPathname - API pathname to send POST request
 * @param {String} modalID - Modal ID too hide after submission
 */
function handleEnquiryFormSubmit(formID, tableID, apiPathname, modalID) {
    $(formID).submit(function(e) {
        e.preventDefault();
        const this_ = $(this);
        console.log("Creating enquiry.");
        addNewEnquiryData(tableID, apiPathname, this_.serialize());
        this_.trigger("reset");
        $(modalID).modal("hide");
    })
}
