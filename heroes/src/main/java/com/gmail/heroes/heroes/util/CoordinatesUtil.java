package com.gmail.heroes.heroes.util;

public class CoordinatesUtil {

    public static double distance(double lat1, double lat2, double lon1, double lon2) {
        lon1 = Math.toRadians(lon1);
        lon2 = Math.toRadians(lon2);
        lat1 = Math.toRadians(lat1);
        lat2 = Math.toRadians(lat2);

        double dlon = lon2 - lon1;
        double dlat = lat2 - lat1;
        double a = Math.pow(Math.sin(dlat / ConstantesUtil.number_2), ConstantesUtil.number_2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(dlon / ConstantesUtil.number_2),ConstantesUtil.number_2);

        double c = ConstantesUtil.number_2 * Math.asin(Math.sqrt(a));

        return (c * ConstantesUtil.radiusEarth);
    }
}
