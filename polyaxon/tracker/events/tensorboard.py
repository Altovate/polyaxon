import tracker

from event_manager.events import tensorboard

tracker.subscribe(tensorboard.TensorboardStartedEvent)
tracker.subscribe(tensorboard.TensorboardStartedTriggeredEvent)
tracker.subscribe(tensorboard.TensorboardSoppedEvent)
tracker.subscribe(tensorboard.TensorboardSoppedTriggeredEvent)
tracker.subscribe(tensorboard.TensorboardViewedEvent)
tracker.subscribe(tensorboard.TensorboardNewStatusEvent)
tracker.subscribe(tensorboard.TensorboardSucceededEvent)
tracker.subscribe(tensorboard.TensorboardFailedEvent)
