import {HttpHeaders, HttpParams} from "@angular/common/http";
import {Table} from "primeng/table";

export class RequestUtil {

    static getRequestParams = (table: Table): HttpParams => {
        let params: HttpParams = new HttpParams();
        if (table == null) {
            return params;
        }

        let datatable = table;
        if (datatable == null) {
            return params;
        }

        params = params.append('page', Math.round(datatable.first / datatable.rows).toString());
        params = params.append('size', datatable.rows == null ? null : datatable.rows.toString());

        const direction = datatable.sortOrder === 1 ? 'ASC' : 'DESC';
        params = params.append('sort', datatable.sortField == null ? '' : datatable.sortField + ',' + direction);

        return params;
    };

    static getHttpOptions(){
        return {
            headers: new HttpHeaders({
              'Content-Type': 'application/json'
              },
            )
          };
    }

}
