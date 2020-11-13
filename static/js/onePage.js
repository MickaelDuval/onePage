function getPage(idPage="#"){
    var data = {};
    $("#contenu").html("<p width='100%' class='text-center'>... chargement en cours ...</p>");

    // data.numPage = numPage;

    // // ajouter tous les datas qui trainent dans les formulaires
    // $(".data").each(function(d){
    //     data[this.name] = $(this).val();
    // });

    $.ajax({
        method: "POST",
        data:{
            "idPage":idPage
        },
        url:"/getPage",
        success: function(data){
            $("#contenu").html(data);
        },
        error: function(data){
            $("#contenu").html("<p>Chargement impossible.</p><p>" + data + "</p>");
        }
    
    });
}
