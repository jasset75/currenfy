

function getRate($rate, sell_ccy, buy_ccy){
    var rateURL = $rate.attr('data-source');
    alert(rateURL);
    // loading CCY Symbols
    $.ajax({
        url: rateURL
    }).then(function(data) {
        $rate.value(data['rate']);
    });    

}

/**
 * 
 * @param {*} $select form select to load symbols
 */
function getFixerSymbols($select){
    // loading CCY Symbols
    $.ajax({
        url: $select.attr('data-source')
    }).then(function(data) {
        // empty selected option
        var $option = new Option('---', '---', selected=true);
        $select.append($option);
        // currenfy symbols API sall
        data.symbols.forEach(symbol => {
            var $option = new Option(symbol, symbol);
            $select.append($option);
        });
    });    
}

/**
 * 
 * @param {*} $bookedTrades table-div to add booked trades as rows
 */
function getBookedTrades($bookedTrades){
    function appendBookedTrade($row, item, even){
        // Sell CCY
        var $sell_currency = $('<div></div>')
            .addClass('col-sm-2')
            .addClass('col-left')
            .text(item['sell_currency']);
        $row.append($sell_currency);
        // Sell Amount
        var $sell_amount = $('<div></div>')
            .addClass('col-sm-2')
            .addClass('col-left')
            .text(item['sell_amount']);
        $row.append($sell_amount);
        // Buy CCY
        var $buy_currency = $('<div></div>')
            .addClass('col-sm-2')
            .addClass('col-left')
            .text(item['buy_currency']);
        $row.append($buy_currency);
        //  Buy Amount
        var $buy_amount = $('<div></div>')
            .addClass('col-sm-2')
            .addClass('col-left')
            .text(item['buy_amount']);
        $row.append($buy_amount);
        // Rate
        var $rate = $('<div></div>')
            .addClass('col-sm-2')
            .addClass('col-left')
            .text(item['rate']);
        $row.append($rate);
        // Date Booked
        var $date_booked = $('<div></div>')
            .addClass('col-sm-2')
            .addClass('col-center')
            .text(item['date_booked']);
        $row.append($date_booked);
    }
    $.ajax({
        url: $bookedTrades.attr('data-source')
    }).then(function(data) {
        var even = true;
        // empty selected option
        data.forEach(item  => {
            var $row = $('<div></div>')
                    .addClass('row')
                    .addClass('booked-trade-row');
            if (even){
                $row.addClass('booked-trade-row-even')
            } else {
                $row.addClass('booked-trade-row-odd')
            }
            $bookedTrades.append($row);
            appendBookedTrade($row, item);
            even = !even;
        });
    });
}