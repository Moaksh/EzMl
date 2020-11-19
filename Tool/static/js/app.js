
$(window, document, undefined).ready(function () {

    $('input').blur(function () {
        var $this = $(this);
        if ($this.val())
            $this.addClass('used');
        else
            $this.removeClass('used');
    });
    $('textarea').blur(function () {
        var $this = $(this);
        if ($this.val())
            $this.addClass('used');
        else
            $this.removeClass('used');
    });
});


function alert() {
    Swal.fire({
        title: 'Sorry but you can not use these commands, to use them you need to buy the Premium package',
        width: 600,
        padding: '3em',
        background: '#553C9A',
    })
}
Swal.fire({
    title: 'Sorry but you can not use these commands, to use them you need to buy the Premium package',
    width: 600,
    padding: '3em',
    background: '#553C9A',
})


$(document).ready(function ($) {

    $(".trainUp").change(function () {
        var filename = readURL(this);
        $(this).parent().children('span').html(filename);
    });

    function readURL(input) {
        var url = input.value;
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (
            ext == "csv"
        )) {
            var path = $(input).val();
            var filename = path.replace(/^.*\\/, "");
            $('.train span').html('Uploaded Proof : ' + filename);
            return "Selected file : " + filename;
        } else {
            $(input).val("");
            return "Only csv formats are allowed!";
        }
    }

});
$(document).ready(function ($) {

    $(".testUp").change(function () {
        var Trfilename = readURL(this);
        $(this).parent().children('span').html(Trfilename);
    });

    function readURL(input) {
        var url = input.value;
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (
            ext == "csv"
        )) {
            var path = $(input).val();
            var Trfilename = path.replace(/^.*\\/, "");
            $('.test span').html('Uploaded Proof : ' + Trfilename);
            return "Selected file : " + Trfilename;
        } else {
            $(input).val("");
            return "Only csv formats are allowed!";
        }
    }

});

$(document).ready(function ($) {

    $(".imgUp").change(function () {
        var Trfilename = readURL(this);
        $(this).parent().children('span').html(Trfilename);
    });

    function readURL(input) {
        var url = input.value;
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (
            ext == "png" || ext == "jpeg" || ext == "jpg"
        )) {
            var path = $(input).val();
            var Trfilename = path.replace(/^.*\\/, "");
            $('.img span').html('Uploaded Proof : ' + Trfilename);
            return "Selected file : " + Trfilename;
        } else {
            $(input).val("");
            return "Only .png and .jpeg formats are allowed!";
        }
    }

});

$('#pills-tab a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
})



console.log('Hola Amigo')