getMASPoptionSql = 'SELECT idx, name, term, color, stroke from nc_b_disparity_option_t'

updateMASPoptionSql  = 'UPDATE nc_b_disparity_option_t SET disparity_value = %s, disparity_color = %s WHERE disparity_name = %s'