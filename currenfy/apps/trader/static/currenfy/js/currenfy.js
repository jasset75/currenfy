/**
 * currenfy namespace 
 */
var currenfy = currenfy || {};

/**
 *  Join url from parts, only valid to http protocol
 * 
 * @param {string[]} parts - join url parts with slash
 */
currenfy.joinUrlParts = function (parts){
    return parts.join('/').replace(RegExp('/+','g'),'/')
         .replace('http:/','http://');
}

/**
 *   Format number into string representation with n decimals,
 *      decimal and thousand separator
 * 
 * @param {integer} n - length of decimal
 * @param {integer} x - length of whole part
 * @param {string} s - sections delimiter
 * @param {string} c - decimal delimiter
 */
Number.prototype.format = function(n, x, s, c) {

    var re = '\\d(?=(\\d{' + (x||3) + '})+' +(n >0 ? '\\D' : '$') + ')'
    var num = this.toFixed(Math.max(0, ~~n));
    return (c ? num.replace('.', c) : num).replace(new RegExp(re, 'g'), '$&' + (s || ','));
}

/**
 *  Returns a parsed float value from string with decimal and thousand separator
 * 
 * @param {string} value - string of number representation
 */
currenfy.parseCurrencyValue = function(value){

    var num = parseFloat(value.replace(/\./g, '').replace(/,/g,'.'));
    return (num != Number.NaN) ? num : '';
}

/**
 *  Checks well-formed Currency Symbol
 * 
 * @param {string} ccy - Currency symbol: EUR, GBP, USD, etc.
 */
currenfy.checkValidCCYSymbol = function(ccy){

    var re_valid_ccy = /\b[A-Z]{3}\b/;
    return ccy.match(re_valid_ccy)
}

/**
 * Gets exchange rate from API REST currenfy source (powered by fixer.io)
 * 
 * @param {object} $rate - input to fill with result
 * @param {string} sell_ccy - Currency Sell Symbol
 * @param {string} buy_ccy - Currency Buy Symbol
 */
currenfy.getRate = function ($rate, sell_ccy, buy_ccy, callback){
    // basic validation
    if (!currenfy.checkValidCCYSymbol(sell_ccy)){
        throw "Sell Currency symbol not valid."
    }
    if (!currenfy.checkValidCCYSymbol(buy_ccy)){
        throw "Buy Currency symbol not valid."
    }
    // assembling the url
    var rateURL = currenfy.joinUrlParts([$rate.attr('data-source'), sell_ccy, buy_ccy]);
    // loading CCY Symbols
    $.ajax({
        url: rateURL
    }).then(function(data) {
        $rate.val(data['rate'].format(2, 3, '.', ','));
        callback();
    });    
}

/**
 *  Gets list of currency symbols from API REST currenfy source (powered by fixer.io)
 * 
 * @param {object} $select - form select to load symbols
 */
currenfy.getFixerSymbols = function($select){
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

currenfy.postNewTrade= function($form){
    // basic validation
    if (!currenfy.checkValidCCYSymbol($form.find('#sell-currency').val())){
        throw "Sell Currency symbol not valid."
    }
    if (!currenfy.checkValidCCYSymbol($form.find('#buy-currency').val())){
        throw "Buy Currency symbol not valid."
    }
    var res = false;
    var formData = {
        "sell_currency": $form.find('#sell-currency').val(),
        "sell_amount": currenfy.parseCurrencyValue($form.find('#sell-amount').val()).toString(),
        "buy_currency": $form.find('#buy-currency').val(),
        "rate": currenfy.parseCurrencyValue($form.find('#rate').val()).toString(),
        "csrfmiddlewaretoken": $form.children('input[name=csrfmiddlewaretoken]').val(),
    }
    // post trade
    $.post($form.attr('currenfy-action'), formData).done(function(){
        res = true;
        alert( "Data Loaded");
    });
    return res;
}

/**
 *  Gets booked trades from API REST currenfy source
 * 
 * @param {object} $bookedTrades table-div to add booked trades as rows
 */
currenfy.getBookedTrades = function($bookedTrades){
    function appendBookedTrade($row, item, even){
        var sell_amount = parseFloat(item['sell_amount']).format(2, 3, '.', ',');
        var buy_amount = parseFloat(item['buy_amount']).format(2, 3, '.', ',');
        var rate = parseFloat(item['rate']).format(4, 3, '.', ',');
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
            .text(sell_amount);
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
            .text(buy_amount);
        $row.append($buy_amount);
        // Rate
        var $rate = $('<div></div>')
            .addClass('col-sm-2')
            .addClass('col-left')
            .text(rate);
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
