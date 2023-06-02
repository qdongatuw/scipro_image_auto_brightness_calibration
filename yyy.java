	void autoAdjust(ImagePlus imp, ImageProcessor ip) {
 		if (RGBImage)
			ip.reset();
		Calibration cal = imp.getCalibration();
		imp.setCalibration(null);
		ImageStatistics stats = imp.getStatistics(); // get uncalibrated stats
		imp.setCalibration(cal);
		int[] histogram = stats.histogram;
		int threshold = stats.pixelCount/5000;
		int i = -1;
		boolean found = false;
		do {
			i++;
			found = histogram[i] > threshold;
		} while (!found && i<255);
		int hmin = i;
		i = 256;
		do {
			i--;
			found = histogram[i] > threshold;
		} while (!found && i>0);
		int hmax = i;
		if (hmax>hmin) {
			imp.killRoi();
			min = stats.histMin+hmin*stats.binSize;
			max = stats.histMin+hmax*stats.binSize;
			ip.setMinAndMax(min, max);
		}
		updateScrollBars();
		Roi roi = imp.getRoi();
		if (roi!=null) {
			int[] mask = roi.getMask();
			if (mask!=null)
				ip.reset(mask);
		}
	}