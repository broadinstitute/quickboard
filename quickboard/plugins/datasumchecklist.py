from quickboard.plugins import DataFilterChecklist


class DataSumChecklist(DataFilterChecklist):
    # Overrides parent method
    def data_transform(self, df, control_value):
        """
        Transforms data so that given column becomes the sum of the values given by `col-name_checklist-item` where
        checklist-item is currently checked.
        """
        df[self.data_col] = 0
        for cv in control_value:
            df[self.data_col] += df[self.data_col + '_' + cv]

        return df
