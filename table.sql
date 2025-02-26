CREATE TABLE cp_r_coin_list_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(255),
    warning VARCHAR(255),
    delflag INT
);

CREATE TABLE cp_p_coin_current_candle_price_t (
    coin_name VARCHAR(255) PRIMARY KEY,
    stime INT,
    open_price VARCHAR(255),
    close_price VARCHAR(255),
    high_price VARCHAR(255),
    low_price VARCHAR(255),
    volume VARCHAR(255),
    time_stamp VARCHAR(255),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_b_search_option_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    create_date VARCHAR(255),
    update_date VARCHAR(255)
);

CREATE TABLE cp_c_pr_price_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    low_price INT,
    high_price INT,
    flag INT
);

CREATE TABLE cp_c_pr_transaction_amount_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    chart_term VARCHAR(255),
    low_transaction_amount INT,
    high_transaction_amount INT,
    flag INT
);

CREATE TABLE cp_c_masp_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    chart_term VARCHAR(255),
    first_disparity INT,
    second_disparity INT,
    comparison VARCHAR(255),
    flag INT
);

CREATE TABLE cp_c_disparity_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    chart_term VARCHAR(255),
    disparity_term VARCHAR(255),
    low_disparity INT,
    high_disparity INT,
    flag INT
);

CREATE TABLE cp_c_trend_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    chart_term VARCHAR(255),
    masp INT,
    trend_term INT,
    trend_reverse INT,
    trend_type VARCHAR(255),
    flag INT
);

CREATE TABLE cp_c_macd_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    chart_term VARCHAR(255),
    short_disparity INT,
    long_disparity INT,
    up_down VARCHAR(255),
    signal INT,
    flag INT
);

CREATE TABLE cp_p_min_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    stime INT,
    open_price VARCHAR(255),
    close_price VARCHAR(255),
    high_price VARCHAR(255),
    low_price VARCHAR(255),
    volume VARCHAR(255),
    coin_name VARCHAR(255),
    time_stamp VARCHAR(255),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_f_recommend_coin_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(255),
    catch_price VARCHAR(255),
    option_name VARCHAR(255)
);

CREATE TABLE cp_p_coin_current_price_t (
    coin_name VARCHAR(255) PRIMARY KEY,
    s_time INT,
    time_stamp VARCHAR(255),
    open_price FLOAT,
    close_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    volume FLOAT,
    transaction_amount FLOAT
);

CREATE TABLE cp_b_trading_option_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    insert_time VARCHAR(255),
    update_time VARCHAR(255)
);

CREATE TABLE cp_c_account_option_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    price_count INT,
    loss_cut_under_percent INT,
    loss INT,
    loss_cut_under_call_price_sell_all INT,
    loss_cut_under_coin_specific_percent INT,
    loss_cut_under_call_price_specific_coin INT,
    loss_cut_over_percent INT,
    gain INT,
    loss_cut_over_call_price_sell_all INT,
    loss_cut_over_coin_specific_percent INT,
    loss_cut_over_call_price_specific_coin INT,
    buy_cancle_time INT,
    sell_cancle_time INT,
    loss INT,
    gain INT
);

CREATE TABLE cp_c_buy_option_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    percent_to_buy_method INT,
    price_to_buy_method INT,
    callmoney_to_buy_method INT,
    checkbox INT
);

CREATE TABLE cp_c_sell_option_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    upper_percent_to_price_condition INT,
    down_percent_to_price_condition INT,
    disparity_for_upper_case INT,
    upper_percent_to_disparity_condition INT,
    disparity_for_down_case INT,
    down_percent_to_disparity_condition INT,
    call_money_to_sell_method VARCHAR(255),
    percent_to_split_sell INT,
    shot_macd_value INT,
    long_macd_value INT,
    macd_signal_value INT,
    trailing_start_percent VARCHAR(255),
    trailing_stop_percent VARCHAR(255),
    trailing_order_call_price VARCHAR(255)
);

CREATE TABLE cp_r_possession_coin_t (
    coin VARCHAR(255),
    user_idx INT,
    unit VARCHAR(255),
    price VARCHAR(255),
    total VARCHAR(255),
    fee VARCHAR(255),
    status INT,
    transaction_time VARCHAR(255),
    conclusion_time VARCHAR(255),
    order_id VARCHAR(255),
    cancel_time VARCHAR(255),
    macd_chart VARCHAR(255),
    disparity_chart VARCHAR(255),
    option_name VARCHAR(255),
    trailingstop_flag INT,
    max_price VARCHAR(255),
    PRIMARY KEY (coin, user_idx)
);

CREATE TABLE cp_b_user_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    active INT,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    salt VARCHAR(255),
    public_key VARCHAR(255) DEFAULT NULL,
    secret_key VARCHAR(255) DEFAULT NULL,
    search_option INT DEFAULT NULL,
    trading_option INT DEFAULT NULL,
    jwt_token VARCHAR(255) DEFAULT NULL,
    refresh_token VARCHAR(255) DEFAULT NULL
);

CREATE TABLE cp_r_coin_list_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(100),
    kr_name VARCHAR(100),
    warning VARCHAR(100),
    delflag INT
);

CREATE TABLE cp_p_coin_current_candle_price_t (
    coin_name VARCHAR(100) PRIMARY KEY,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_b_use_search_option_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    search_idx INT
);

CREATE TABLE cp_b_disparity_option_t (
    disparity_idx INT PRIMARY KEY AUTO_INCREMENT,
    disparity_name VARCHAR(100),
    disparity_color VARCHAR(100),
    disparity_value VARCHAR(100)
);

CREATE TABLE cp_p_min_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_p_3min_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_p_5min_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_p_10min_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_p_30min_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_p_1H_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100)
);

CREATE TABLE cp_p_6H_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_p_12H_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_p_1D_bithumb_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    s_time INT,
    open_price VARCHAR(100),
    close_price VARCHAR(100),
    high_price VARCHAR(100),
    low_price VARCHAR(100),
    volume VARCHAR(100),
    coin_name VARCHAR(100),
    time VARCHAR(100),
    empty_count INT DEFAULT 0
);

CREATE TABLE cp_f_recommend_coin_list_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(100),
    catch_price VARCHAR(100),
    option_name VARCHAR(100)
);

CREATE TABLE cp_p_coin_current_price_t (
    coin_name VARCHAR(100) PRIMARY KEY,
    s_time INT,
    time VARCHAR(100),
    open_price FLOAT,
    close_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    volume FLOAT,
    transaction_amount FLOAT
);

CREATE TABLE cp_p_1m_coin_price_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(100),
    s_time INT,
    time VARCHAR(100),
    open_price FLOAT,
    close_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    ask_price FLOAT,
    avg_price FLOAT,
    volume FLOAT,
    transaction_amount FLOAT,
    disparity FLOAT
);

CREATE TABLE cp_p_30m_coin_price_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(100),
    s_time INT,
    time VARCHAR(100),
    open_price FLOAT,
    close_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    ask_price FLOAT,
    avg_price FLOAT,
    volume FLOAT,
    transaction_amount FLOAT,
    disparity FLOAT
);

CREATE TABLE cp_p_1h_coin_price_t (
    idx INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(100),
    s_time INT,
    time VARCHAR(100),
    open_price FLOAT,
    close_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    ask_price FLOAT,
    avg_price FLOAT,
    volume FLOAT,
    transaction_amount FLOAT,
    disparity FLOAT
);
