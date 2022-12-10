from dto_pack import TransferTransitionTrigger, TransferStatus

TransferStatusTransitions = [
    # Main Flow
    [TransferTransitionTrigger.Submit, TransferStatus.Init, TransferStatus.Pending],
    [TransferTransitionTrigger.Cancel, TransferStatus.Pending, TransferStatus.Canceled],
    [TransferTransitionTrigger.Transferred, TransferStatus.Pending, TransferStatus.Succeed],
    [TransferTransitionTrigger.Failed, TransferStatus.Pending, TransferStatus.Failed]
]