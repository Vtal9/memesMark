import React from 'react'
import { FormControlLabel, Switch, Typography } from '@material-ui/core'


type MySwitchProps = {
  value: boolean
  onChange: (newValue: boolean) => void
  label: string
}

const MySwitch: React.FC<MySwitchProps> = props => (
  <FormControlLabel
    control={
      <Switch
        color='primary'
        checked={props.value}
        onChange={e => props.onChange(e.target.checked)}
      />
    } label={
      <Typography color={props.value ? 'textPrimary' : 'textSecondary'}>{props.label}</Typography>
    }
  />
)

export default MySwitch