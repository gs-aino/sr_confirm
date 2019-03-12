$('#sr_table tbody').on( 'click', 'tr', function () {

    var table = $('#sr_table').DataTable();

    if ( $(this).hasClass('selected') ) {
        $(this).removeClass('selected');
        $(this).addClass('selected');
    }
    else {
        table.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
    }

    var sr_no = $('tr.selected > td:nth-child(2)').text();
    console.log("#sr_analysis_info");
    console.log(sr_no);

    $.ajax({
        url: "/sr_analysis_info",
        processData: false,
        contentType: false,
        type: "POST",
        data : sr_no,
        success : function(json_text){
            var data = $.parseJSON(json_text);
            // console.log(data);
            setAnalysisBox(data);
        },
        error: function(err){
          console.log(err);
        }
    })
} );


function setAnalysisBox(data){
  console.log(data);

  $('#tag_box').css("display", "block");
  $('#first_tag').text(data.tag_first_name);
  $('.first_per').text(data.tag_first_prob.toFixed(2));

  $('#second_tag').text(data.tag_second_name);
  $('.second_per').text(data.tag_second_prob.toFixed(2));

  $('#third_tag').text(data.tag_third_name);
  $('.third_per').text(data.tag_third_prob.toFixed(2));


  $('#customer_keywords').text(data.kwd_cust_confirm);
  $('#gs_keywords').text(data.kwd_gs_confirm);


  $('#cust_gs_text').html('고객 : '+data.customer_text + '<br> '+'GS : '+ data.gs_text );
  // let key_arr = data.kwd_cust_origin;
  // for(let i = 0; i < key_arr.length; i ++){
  //   let tag = `<span class="amsify-select-tag col-bg" data-val="${key_arr[i]}">${key_arr[i]}<b class="amsify-remove-tag">✖</b></span>`;
  //   $('#customer_tag').siblings('.amsify-suggestags-area').find('.amsify-suggestags-input-area-default').prepend(tag);
  // }

}
// $(document).ready(function() {
    // var table = $('#sr_table').DataTable();

    // $('#sr_table tbody').on( 'click', 'tr', function () {
    //     var table = $('#sr_table');
    //     if ( $(this).hasClass('selected') ) {
    //         $(this).removeClass('selected');
    //         let this_sr_no = $('tr.selected').nth_child(2).val();
    //         console.log("click");
    //
    //         $.ajax({
    //             url: "{{ url_for('sr_analysis_info') }}",
    //             processData: false,
    //             contentType: false,
    //             type: "POST",
    //             data : {"sr_no" : this_sr_no},
    //             dataType : 'json',
    //             // success: function(data){
    //             //   setAnalysisBox(data);
    //             // },
    //             error: function(err){
    //               console.log('s');
    //               console.log(err);
    //             }
    //           })
    //     }
    //     else {
    //         table.$('tr.selected').removeClass('selected');
    //         $(this).addClass('selected');
    //     }
    // } );
// } );
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
