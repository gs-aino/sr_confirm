$(document).ready(function() {
    var table = $('#example').DataTable();

    $('#example tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );
} );
//  $(document).ready(function () {
//  // var zip = (...rows) => [...rows[0]].map((_,c) => rows.map(row => row[c]));
// function zip() {
//     var args = [].slice.call(arguments);
//     var shortest = args.length==0 ? [] : args.reduce(function(a,b){
//         return a.length<b.length ? a : b
//     });
//
//     return shortest.map(function(_,i){
//         return args.map(function(array){return array[i]})
//     });
// }
//
// $('#sentiment_button').click(function () {
//     console.log('button clicked');
//
//     var input_text = $('#input_text').val();
//
//     // TODO modal and progress bar for ver_2
//     // $('.js-loading-bar').modal({
//     //     backdrop: 'static',
//     //     show: false
//     // });
//     // var $modal = $('#page_loading');
//     // var $bar= $modal.find('.progress-bar');
//     //
//     // $modal.modal('show');
//     // $bar.addClass('animate');
//
//
//     $.ajax({
//         url: '/sr_test/sentiment_analysis',
//         data: {'input_text': input_text},
//         type: 'POST',
//         beforeSend: function(){
//             $('#sentiment_box').addClass("display-none");
//             $('#coloured_text').val("");
//             $('#sentiment_table tbody').html("");
//         },
//         success: function (_res) {
//             // TODO modal and progress bar for ver_2
//             // $bar.removeClass('animate');
//             // $modal.modal('hide');
//
//             var res = JSON.parse(_res);
//             console.log(res);
//
//             $('#sentiment_total_score h4').text(res['total_score']);
//
//             var word_list = res['word_list'];
//             // console.log(word_list);
//
//             var score_list = res['score_list'];
//             // console.log(score_list);
//
//             $('#coloured_text').val(res['coloured_text']);
//
//             // distribute data
//             var temp_html = '';
//             zip(word_list, score_list).forEach(
//                 function (elements) {
//                     var word = elements[0];
//                     var score = String(elements[1]);
//                     console.log(temp_html);
//                     temp_html = temp_html.concat('<tr><td>', word, '</td><td>', score, '</td></tr>');
//                 }
//             );
//
//             // console.log(temp_html);
//             $('#sentiment_table tbody').html(temp_html);
//         },
//         complete:function () {
//             var len = (document.getElementById("sentiment_table")
//                 .getElementsByTagName("tr").length - 1)
//                 .toString();
//             // console.log(len);
//
//             // row span
//             $('#sentiment_table > tbody > tr:nth-child(1) > td:nth-child(1)')
//                 .before('<td rowspan="' + len + '">'+ $("#coloured_text").val() +'</td>');
//             $('#sentiment_box').removeClass("display-none");
//         }
//     })
// });
// });
