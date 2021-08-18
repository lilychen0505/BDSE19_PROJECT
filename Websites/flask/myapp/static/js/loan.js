
function ChangeString() {
    const monetary = document.getElementById("monetary").value;
    const years = document.getElementById("years").value;

    const monetary_new = monetary * 10000;
    const months = years * 12;

    // 每月應付本息金額之平均攤還率 ＝{[(1＋月利率)^月數]×月利率}÷{[(1＋月利率)^月數]－1};  

    // 1王道銀行 階梯利率信貸
    const interest_rate1 = 0.022; //7800
    const avg_interest_rate1 = (Math.pow(1 + (interest_rate1 / 12), months) * interest_rate1 / 12) / (Math.pow(1 + (interest_rate1 / 12), months) - 1);
    const payment_monthly1 = Math.ceil(monetary_new * avg_interest_rate1);

            // 2滙豐銀行 閃光0.1%專案
    const interest_rate2 = 0.0278; //3000
    const avg_interest_rate2 = (Math.pow(1 + (interest_rate2 / 12), months) * interest_rate2 / 12) / (Math.pow(1 + (interest_rate2 / 12), months) - 1);
    const payment_monthly2 = Math.ceil(monetary_new * avg_interest_rate2);

            // 3永豐銀行 數時貸
    const interest_rate3 = 0.0345; //888
    const avg_interest_rate3 = (Math.pow(1 + (interest_rate3 / 12), months) * interest_rate3 / 12) / (Math.pow(1 + (interest_rate3 / 12), months) - 1);
    const payment_monthly3 = Math.ceil(monetary_new * avg_interest_rate3);

            // 4凱基銀行 優利貸款
    const interest_rate4 = 0.0232; //3000 
    const avg_interest_rate4 = (Math.pow(1 + (interest_rate4 / 12), months) * interest_rate4 / 12) / (Math.pow(1 + (interest_rate4 / 12), months) - 1);
    const payment_monthly4 = Math.ceil(monetary_new * avg_interest_rate4);

            // 5國泰世華 大樹速貸
    const interest_rate5 = 0.0336; //5000
    const avg_interest_rate5 = (Math.pow(1 + (interest_rate5 / 12), months) * interest_rate5 / 12) / (Math.pow(1 + (interest_rate5 / 12), months) - 1);
    const payment_monthly5 = Math.ceil(monetary_new * avg_interest_rate5);

            // 6上海商銀 優利貸
    const interest_rate6 = 0.0262; //3000
    const avg_interest_rate6 = (Math.pow(1 + (interest_rate6 / 12), months) * interest_rate6 / 12) / (Math.pow(1 + (interest_rate6 / 12), months) - 1);
    const payment_monthly6 = Math.ceil(monetary_new * avg_interest_rate6);

            // 7新光銀行 優質卡友專案
    const interest_rate7 = 0.0364; //3000
    const avg_interest_rate7 = (Math.pow(1 + (interest_rate7 / 12), months) * interest_rate7 / 12) / (Math.pow(1 + (interest_rate7 / 12), months) - 1);
    const payment_monthly7 = Math.ceil(monetary_new * avg_interest_rate7);

            // 8聯邦銀行 好好貸款
    const interest_rate8 = 0.0347; //5000
    const avg_interest_rate8 = (Math.pow(1 + (interest_rate8 / 12), months) * interest_rate8 / 12) / (Math.pow(1 + (interest_rate8 / 12), months) - 1);
    const payment_monthly8 = Math.ceil(monetary_new * avg_interest_rate8);

    document.getElementById("NewStringBox").innerHTML = "每月還款額: $" + payment_monthly1 + "元起，詳請請見下表";
    document.getElementById("box1").innerHTML = "每月最低還款額: $" + payment_monthly1 + "元";
    document.getElementById("box2").innerHTML = "每月最低還款額: $" + payment_monthly2 + "元";
    document.getElementById("box3").innerHTML = "每月最低還款額: $" + payment_monthly3 + "元";
    document.getElementById("box4").innerHTML = "每月最低還款額: $" + payment_monthly4 + "元";
    document.getElementById("box5").innerHTML = "每月最低還款額: $" + payment_monthly5 + "元";
    document.getElementById("box6").innerHTML = "每月最低還款額: $" + payment_monthly6 + "元";
    document.getElementById("box7").innerHTML = "每月最低還款額: $" + payment_monthly7 + "元";
    document.getElementById("box8").innerHTML = "每月最低還款額: $" + payment_monthly8 + "元";




    }