const address = window.location;

document.querySelectorAll("#messages").forEach(function(message) {
    setTimeout(function() {
        $(message).fadeOut("slow");
    }, 3000)
});


$("#ota-link,#partners-link,#review-link").click(function(e) {
    e.preventDefault();

    const this_ = $(this);

    // Get the pathname in order to refer which data is to be fetched i.e ota or partner or review, etc
    let pathname = this_.attr("href").split("/");

    // get the type of data to be fetched i.e ota or partner etc
    const dataType = pathname[pathname.length-2];
    console.log(dataType);

    // Insert the 'j' at the to match the view data
    // Eg- /enquiry/j/ota/  or /enquiry/j/partner
    pathname.splice(2, 0, "j");

    // Complete URL to fetch the data
    const contentFetchURL = address.origin + pathname.join("/");
    console.log(contentFetchURL);


    $.ajax({
        url: contentFetchURL,
        method: "GET",
        success: function(data) {
            // Change the title of the page
            document.title = `S3 Infosoft - ${dataType[0].toUpperCase() + dataType.substring(1)}`;

            // Change the address of the page
            window.history.pushState(data, null, this_.attr("href"));
            $(".container-fluid").html(data);
        },
        error: function(err) {
            console.log(err);
        }
    })
});