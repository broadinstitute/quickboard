from quickboard.plugins import DataFilterChecklist


class DataSumChecklist(DataFilterChecklist):
    # Overrides parent method
    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Transforms data so that given column becomes the sum of the values given by `col-name_checklist-item` where
        checklist-item is currently checked.
        """
        data_col = control_attributes['data_col']
        df[data_col] = 0
        for cv in control_value:
            df[data_col] += df[data_col + '_' + cv]

        return df, {}
